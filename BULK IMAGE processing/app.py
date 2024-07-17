from flask import Flask, render_template, jsonify
import random

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Mock data for demonstration
image_paths = [
    '/img/1.jpeg', '/img/2.jpeg', '/img/3.jpeg', '/img/4.jpeg', '/img/5.jpeg',
    '/img/6.jpeg', '/img/7.jpeg', '/img/8.jpeg', '/img/9.jpeg', '/img/10.jpeg',
    '/img/11.jpeg', '/img/12.jpeg', '/img/13.jpeg', '/img/14.jpeg', '/img/15.jpeg',
    '/img/16.jpeg', '/img/17.jpeg', '/img/18.jpeg', '/img/19.jpeg', '/img/20.jpeg',
    '/img/21.jpeg', '/img/22.jpeg', '/img/23.jpeg', '/img/24.jpeg', '/img/25.jpeg',
    '/img/26.jpeg', '/img/27.jpeg', '/img/28.jpeg', '/img/29.jpeg', '/img/30.jpeg',
    '/img/31.jpeg', '/img/32.jpeg', '/img/33.jpeg', '/img/34.jpeg', '/img/35.jpeg',
    '/img/36.jpeg', '/img/37.jpeg', '/img/38.jpeg', '/img/39.jpeg', '/img/40.jpeg',
    '/img/41.jpeg', '/img/42.jpeg', '/img/43.jpeg', '/img/44.jpeg', '/img/45.jpeg',
    '/img/46.jpeg', '/img/47.jpeg', '/img/48.jpeg', '/img/49.jpeg', '/img/50.jpeg'
]

def process_image(image_path):
    execution_time_ms = random.randint(100, 500)
    job_id = image_path.split('/')[-1]
    view_original_link = f'/view_original/{job_id}'
    view_processed_link = f'/view_processed/{job_id}'

    # Simulated detected objects
    objects = ['Tree', 'dog', 'Flower', 'IceCream', 'Man']
    list_of_objects = [random.choice(objects) for _ in range(random.randint(0, 2))]
    status = 'Processed' if list_of_objects else 'Queue'

    return {
        'image_name': job_id,
        'job_id': job_id,
        'execution_time_ms': execution_time_ms,
        'view_original': view_original_link,
        'view_processed': view_processed_link,
        'list_of_objects': list_of_objects,
        'status': status
    }

def generate_reports(results):
    summary_report = generate_summary_report(results)
    detailed_report = results  # No need to modify detailed report for pagination here
    return summary_report, detailed_report

def generate_summary_report(results):
    total_images = len(results)
    total_processed = sum(1 for result in results if result['status'] == 'Processed')
    total_queue = sum(1 for result in results if result['status'] == 'Queue')
    total_time = sum(result['execution_time_ms'] for result in results)
    in_processing_queue = total_queue  # Number of images in the queue
    total_remaining = total_queue  # Total remaining is the same as the number in the queue

    return {
        'total_images': total_images,
        'total_processed': total_processed,
        'total_time': format_time(total_time),
        'total_remaining': total_remaining,
        'in_processing_queue': in_processing_queue,
        'total_celery_workers': 10,  # Example value
        'total_yolo_models': 5,  # Example value
    }

def format_time(milliseconds):
    seconds = milliseconds / 1000
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h)}h:{int(m)}m:{int(s)}s:{int((seconds - int(seconds)) * 1000)}ms"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_images', methods=['POST'])
def process_images():
    results = [process_image(path) for path in image_paths]
    summary_report, detailed_report = generate_reports(results)
    return jsonify({
        'summary_report': summary_report,
        'detailed_report': detailed_report
    })

if __name__ == "__main__":
    app.run(debug=True)
