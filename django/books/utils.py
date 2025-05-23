from gtts import gTTS
from io import BytesIO
from django.core.files.base import ContentFile

def generate_audio_for_book(book):
    # 책 설명 텍스트를 받아서 음성 생성
    tts = gTTS(text=book.description, lang='ko')  # 한국어
    audio_io = BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)

    filename = f'audio_{book.id}.mp3'

    # 기존 오디오가 있으면 삭제
    if book.audio_file:
        book.audio_file.delete(save=False)

    # 새 오디오 저장
    book.audio_file.save(filename, ContentFile(audio_io.read()), save=True)
