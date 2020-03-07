
class Options:
    save_outputs = False
    save_logos = True
    save_text_images = True
    save_character_images = False
    log_logos_service = True
    log_logos_service_file = 'data/logs/logo.log'
    log_ocr_service = True
    allowed_extensions = ['avi', 'mp4']
    upload_folder = 'upload/'
    default_video = 'upload/Bundesliga-Goals.mp4'
    detection_service_port = "8080"
    logo_service_port = "1721"
    ocr_service_port = "1720"


Config = Options()
