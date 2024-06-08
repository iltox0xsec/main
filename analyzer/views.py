from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import uuid
from django.urls import reverse
from .forms import *
from .utils import *
import email
from email import policy
from email.parser import BytesParser
import re, os
import base64
from tempfile import NamedTemporaryFile
from django.conf import settings



def index(request):
    return render(request, 'analyzer/index.html')

def parse_received_header(header):
    hop_data = {
        'Hop': None,
        'From': None,
        'By': None,
        'With': None,
        'Date (UTC)': None,
        'Delay': None
    }
    
    hop_match = re.search(r'hop\s+(\d+)', header, re.IGNORECASE)
    if hop_match:
        hop_data['Hop'] = hop_match.group(1)
    
    from_match = re.search(r'from\s+([^\s]+)', header, re.IGNORECASE)
    if from_match:
        hop_data['From'] = from_match.group(1)
    
    by_match = re.search(r'by\s+([^\s]+)', header, re.IGNORECASE)
    if by_match:
        hop_data['By'] = by_match.group(1)
    
    with_match = re.search(r'with\s+([^\s]+)', header, re.IGNORECASE)
    if with_match:
        hop_data['With'] = with_match.group(1)
    
    date_match = re.search(r';\s+(.*)', header)
    if date_match:
        hop_data['Date (UTC)'] = date_match.group(1)
    
    delay_match = re.search(r'delay\s+(\d+)', header, re.IGNORECASE)
    if delay_match:
        hop_data['Delay'] = delay_match.group(1)
    
    return hop_data

    
def extract_info_from_eml(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    info = {}

    # Headers
    info['Message_ID'] = msg.get('Message-ID', 'N/A')
    info['Subject'] = msg.get('Subject', 'N/A')
    info['Date_UTC'] = msg.get('Date', 'N/A')
    info['From'] = msg.get('From', 'N/A')
    info['To'] = msg.get('To', 'N/A')

    # Hops
    import re

    # Regex pattern to extract relevant parts from Received headers
    received_pattern = re.compile(
        r"from\s+(?P<from>\S+)\s+by\s+(?P<by>\S+)\s+with\s+(?P<with>\S+)\s+id\s+(?P<id>\S+)\s+;\s+(?P<date>.*)"
    )

    hops = []
    received_headers = msg.get_all('Received')
    if received_headers:
        for received in received_headers:
            hop_data = parse_received_header(received)
            hops.append(hop_data)
    info['Hops'] = hops

    # X headers
    x_headers = {}
    for header in msg.keys():
        if header.startswith('x-'):
            x_headers[header] = msg[header]
    info['X_headers'] = x_headers

    # Other headers
    other_headers = {}
    for header in msg.keys():
        if not header.startswith('x-') and header not in ['Message-ID', 'Subject', 'Date', 'From', 'To', 'Received']:
            other_headers[header] = msg[header]
    info['Other_headers'] = other_headers

    # Bodies
    info['Bodies'] = {}
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == 'text/plain':
                info['Bodies']['text/plain'] = part.get_payload(decode=True).decode(part.get_content_charset())
            elif part.get_content_type() == 'text/html':
                info['Bodies']['text/html'] = part.get_payload(decode=True).decode(part.get_content_charset())
    else:
        if msg.get_content_type() == 'text/plain':
            info['Bodies']['text/plain'] = msg.get_payload(decode=True).decode(msg.get_content_charset())
        elif msg.get_content_type() == 'text/html':
            info['Bodies']['text/html'] = msg.get_payload(decode=True).decode(msg.get_content_charset())


    # Extract URLs
    urls = re.findall(r'(https?://\S+)', info['Bodies'].get('text/html', ''))
    info['Extracted_URLs'] = urls

    # Extract emails
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', info['Bodies'].get('text/html', ''))
    info['Extracted_emails'] = emails

    # Extract domains
    domains = re.findall(r'https?://([A-Za-z0-9.-]+)', info['Bodies'].get('text/html', ''))
    info['Extracted_domains'] = domains


    return info

def upload_eml(request):
    if request.method == 'POST':
        form = EmlUploadForm(request.POST, request.FILES)
        if form.is_valid():
            eml_file = request.FILES['eml_file']
            if eml_file.name.endswith('.eml'):
                fs = FileSystemStorage()
                file_path = f"eml/{uuid.uuid4()}.eml"
                filename = fs.save(file_path, eml_file)
                uploaded_file_url = fs.url(filename)

                return redirect(reverse('analyzer:show_result', kwargs={'uploaded_file_url': filename}))
            else:
                form.add_error('eml_file', 'Yalnızca .eml dosyaları yükleyebilirsiniz.')
    else:
        form = EmlUploadForm()
    return render(request, 'analyzer/eml/upload_eml.html', {'form': form})

def show_result(request, uploaded_file_url):
    file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file_url)
    try:
        info = extract_info_from_eml(file_path)
        #print("Extracted Info:", info)  # Debug Output
    except Exception as e:
        print("Error extracting EML info:", e)
        info = {}
    return render(request, 'analyzer/eml/result.html', {'info': info})



# UploadAnyFile



def handle_uploaded_any_file(f):
    file_name = f.name
    content_type = f.content_type
    file_content = f.read()

    response_text = f"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <div class="container" style="margin-top: 20px;">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">File Information</h2>
                <p><strong>File Name:</strong> {file_name} <button class="btn btn-sm btn-primary" onclick="copyToClipboard('file-name', this)">Copy</button></p>
                <p id="file-name" style="display: none;">{file_name}</p>
                <p><strong>Content Type:</strong> {content_type} <button class="btn btn-sm btn-primary" onclick="copyToClipboard('content-type', this)">Copy</button></p>
                <p id="content-type" style="display: none;">{content_type}</p>
    """

    if len(file_content) > 1024 * 1024:  # 1 MB
        file_path = os.path.join(settings.TEMP_DIR, f"{uuid.uuid4()}_{file_name}.txt")
        with open(file_path, 'wb') as tmp_file:
            tmp_file.write(file_content)
        response_text += f"""
                <p>File is too large. Download it <a class="badge btn btn-large badge-success" href='/analyzer/download/file-analyze/?file_path={file_path}'> HERE</a> .</p>
            </div>
        </div>
    </div>
        """
    else:
        file_content_base64 = base64.b64encode(file_content).decode('utf-8')
        response_text += f"""
                <p><strong>File Content (Base64):</strong></p>
                <textarea id="file-content" class="form-control" rows="10">{file_content_base64}</textarea>
                <button class="btn btn-sm btn-primary mt-2" onclick="copyToClipboard('file-content', this)">Copy Content</button>
                <button class="btn btn-sm btn-secondary mt-2" onclick="decodeBase64('file-content', 'decoded-content', this)">Decode Content</button>
                <div id="loading" class="mt-2" style="display: none;">Decoding, please wait...</div>
                <textarea id="decoded-content" class="form-control mt-2" rows="10" style="display: none;"></textarea>
                <button id="copy-decoded-content" class="btn btn-sm btn-primary mt-2" style="display: none;" onclick="copyToClipboard('decoded-content', this)">Copy Decoded Content</button>
            </div>
        </div>
    </div>
        """

    response_text += """
    <script>
        function copyToClipboard(elementId, button) {
            var copyText = document.getElementById(elementId).value;
            navigator.clipboard.writeText(copyText).then(function() {
                var originalText = button.innerText;
                button.innerText = 'Copied';
                setTimeout(function() {
                    button.innerText = originalText;
                }, 2000);
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        }

        function decodeBase64(inputElementId, outputElementId, button) {
            var encodedText = document.getElementById(inputElementId).value;
            var loadingElement = document.getElementById('loading');
            var outputElement = document.getElementById(outputElementId);

            loadingElement.style.display = 'block';
            button.disabled = true;

            setTimeout(function() {
                try {
                    var decodedText = atob(encodedText);
                    loadingElement.style.display = 'none';
                    outputElement.style.display = 'block';
                    outputElement.value = decodedText;
                    button.disabled = false;
                    document.getElementById('copy-decoded-content').style.display = 'inline-block';
                } catch (e) {
                    console.error('Could not decode base64 text: ', e);
                    alert('Invalid base64 content');
                    loadingElement.style.display = 'none';
                    button.disabled = false;
                }
            }, 100);  // Simulate delay for decoding
        }
    </script>
    """

    return HttpResponse(response_text)

def upload_any_file(request):
    if request.method == 'POST':
        form = UploadAnyFileForm(request.POST, request.FILES)
        if form.is_valid():
            return handle_uploaded_any_file(request.FILES['file'])
    else:
        form = UploadAnyFileForm()
    return render(request, 'analyzer/anyfile/upload_any_file.html', {'form': form})

def download_any_file(request):
    file_path = request.GET.get('file_path')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    else:
        return HttpResponse("File not found.", status=404)


# JWT


def jwt(request):
    return render(request, 'analyzer/jwt/index.html') 

def analyze_jwt(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        header, payload, valid = decode_jwt(token)
        response = {
            'header': header,
            'payload': payload,
            'valid': valid
        }
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)