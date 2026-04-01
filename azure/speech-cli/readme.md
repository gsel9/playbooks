# Speech-enabled apps with Microsoft Foundry

Azure AI Speech is a service that provides speech-related functionality, including:
- A speech-to-text API that enables you to implement speech recognition (converting audible spoken words into text).
- A text-to-speech API that enables you to implement speech synthesis (converting text into audible speech).

Before you can use Azure Speech, you need to create an Azure Speech resource in your Azure subscription. You can use either
- a dedicated Azure Speech resource 
- a Microsoft Foundry resource.

After you create your resource, you'll need the following information to use it from a client application through one of the supported SDKs:
- The location in which the resource is deployed (for example, eastus)
- One of the keys assigned to your resource.

You can view of these values on the Keys and Endpoint page for your resource in the Azure portal.

## Speech To Text API
While the specific details vary, depending on the SDK being used (Python, C#, and so on); there's a consistent pattern for using the Speech to text API:
1. Use a SpeechConfig object to encapsulate the information required to connect to your Azure Speech resource. Specifically, its location and key.
2. Optionally, use an AudioConfig to define the input source for the audio to be transcribed. By default, this is the default system microphone, but you can also specify an audio file.
3. Use the SpeechConfig and AudioConfig to create a SpeechRecognizer object. This object is a proxy client for the Speech to text API.
4. Use the methods of the SpeechRecognizer object to call the underlying API functions. For example, the RecognizeOnceAsync() method uses the Azure Speech service to asynchronously transcribe a single spoken utterance.
5. Process the response from the Azure Speech service. In the case of the RecognizeOnceAsync() method, the result is a SpeechRecognitionResult object that includes the following properties:
  - Duration
  - OffsetInTicks
  - Properties
  - Reason
  - ResultId
  - Text
If the operation was successful, the Reason property has the enumerated value RecognizedSpeech, and the Text property contains the transcription. 

## Text To Speech API
The pattern for implementing speech synthesis is similar to that of speech recognition:
1. Use a SpeechConfig object to encapsulate the information required to connect to your Azure Speech resource. Specifically, its location and key.
2. Optionally, use an AudioConfig to define the output device for the speech to be synthesized. By default, this is the default system speaker, but you can also specify an audio file, or by explicitly setting this value to a null value, you can process the audio stream object that is returned directly.
3. Use the SpeechConfig and AudioConfig to create a SpeechSynthesizer object. This object is a proxy client for the Text to speech API.
4. Use the methods of the SpeechSynthesizer object to call the underlying API functions. For example, the SpeakTextAsync() method uses the Azure Speech service to convert text to spoken audio.
5. Process the response from the Azure Speech service. In the case of the SpeakTextAsync method, the result is a SpeechSynthesisResult object that contains the following properties:
  - AudioData
  - Properties
  - Reason
  - ResultId
When speech has been successfully synthesized, the Reason property is set to the SynthesizingAudioCompleted enumeration and the AudioData property contains the audio stream (which, depending on the AudioConfig may have been automatically sent to a speaker or file).

### Audio Format
Choose output formats based on required audio file type, sample-rate, bit-depth. E.g.: Audio16Khz128KBitRateMonoMp3.

### Voices 
Voices are identified by name to indicate a locale (e.g.: en-US) and a person's name. Example: en-GB-George. Speaking style can express emotions like cheerfulness, empathy, and calm. 

## Speech Synthesis Markup Language
Azure Speech SDK enables supports an XML-based syntax for describing characteristics of the speech you want to generate. The Speech Synthesis Markup Language (SSML) syntax offers greater control over how the spoken output sounds, enabling you to:
- Specify a speaking style, such as "excited" or "cheerful" when using a neural voice.
- Insert pauses or silence.
- Specify phonemes (phonetic pronunciations), for example to pronounce the text "SQL" as "sequel".
- Adjust the prosody of the voice (affecting the pitch, timbre, and speaking rate).
- Use common "say-as" rules, for example to specify that a given string should be expressed as a date, time, telephone number, or other form.
- Insert recorded speech or audio, for example to include a standard recorded message or simulate background noise.
