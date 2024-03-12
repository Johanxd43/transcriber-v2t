import subprocess
from typing import Optional


class Transcriber:
    def __init__(self, model):
        """
        Inicializa el transcriptor con un modelo de transcripción específico.
        :param model: Un modelo de transcripción pre-cargado o un identificador para cargar el modelo.
        """
        self.model = self.load_model(model)

    def load_model(self, model_identifier):
        """
        Carga el modelo Whisper basado en un identificador de modelo.
        """
        if model_identifier == "whisper":
            try:
                from whisper import load_model

                model = load_model(
                    "base"
                )  # Puedes elegir entre diferentes versiones del modelo Whisper aquí.
            except ImportError:
                raise ImportError(
                    "No se pudo importar el módulo Whisper. Asegúrate de que esté instalado."
                )
        else:
            raise ValueError(
                f"Modelo de transcripción '{model_identifier}' no soportado."
            )
        return model

    def extract_audio(self, video_path: str, audio_path: Optional[str] = None) -> str:
        """
        Extrae el audio de un archivo de video y lo guarda en un formato de audio específico.
        :param video_path: Ruta al archivo de video.
        :param audio_path: Ruta donde se guardará el archivo de audio extraído. Si es None, se generará automáticamente.
        :return: Ruta al archivo de audio extraído.
        """
        if audio_path is None:
            audio_path = video_path.rsplit(".", 1)[0] + ".wav"
        # Usar FFmpeg para extraer audio. Asegúrate de que FFmpeg esté instalado y disponible en el PATH.
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",
                audio_path,
            ],
            check=True,
        )
        return audio_path

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe el audio a texto utilizando el modelo Whisper cargado.
        """
        try:
            result = self.model.transcribe(audio_path)
            transcribed_text = result["text"]
        except Exception as e:
            raise RuntimeError(f"Error durante la transcripción: {e}")
        return transcribed_text


# Ejemplo de cómo se usaría la clase Transcriber
# transcriber = Transcriber(model="whisper")
# audio_path = transcriber.extract_audio("path/to/video.mp4")
# transcription = transcriber.transcribe(audio_path)
# print(transcription)
