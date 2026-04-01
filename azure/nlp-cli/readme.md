# Natural Language Solutions in Azure

Core apabilities:
* Key phrase extraction is the process of evaluating the text of a document, or documents, and then identifying the main points around the context of the document(s). Key phrase extraction works best for larger documents (the maximum size that can be analyzed is 5,120 characters).
* Sentiment analysis is used to evaluate how positive or negative a text document is. Sentence sentiment is based on confidence scores for positive, negative, and neutral classification values between 0 and 1. Overall document sentiment is based on sentences.
* Named Entity Recognition identifies entities that are mentioned in the text. Entities are grouped into categories and subcategories, for example: Person, Location, DateTime, Organization, Address, Email, URL.
  - In some cases, the same name might be applicable to more than one entity. For example, does an instance of the word "Venus" refer to the planet or the goddess from mythology?
  - Entity linking can be used to disambiguate entities of the same name by referencing an article in a knowledge base.

## Analyze Text

Azure AI Language supports analysis of text, including language detection, sentiment analysis, key phrase extraction, and entity recognition.

For example, suppose a travel agency wants to process hotel reviews that have been submitted to the company's web site. By using the Azure AI Language, they can determine the language each review is written in, the sentiment (positive, neutral, or negative) of the reviews, key phrases that might indicate the main topics discussed in the review, and named entities, such as places, landmarks, or people mentioned in the reviews.

- Requires an Azure Language Resource

## Question-Answering

Azure Language includes a question answering capability, which enables you to define a knowledge base of question and answer pairs that can be queried using natural language input. The knowledge base can be published to a REST endpoint and consumed by client applications, commonly bots.

The knowledge base can be created from existing sources, including:
- Web sites containing frequently asked question (FAQ) documentation.
- Files containing structured text, such as brochures or user guides.
- Built-in chit chat question and answer pairs that encapsulate common conversational exchanges.

Compared to conversational language understanding capabilities, Q&A is a static answer to a known question.

### Create a Question Answering Solution

- In Azure portal, create a Language Service
- Sign in to https://language.cognitive.azure.com/
- Create a new question answering project

## Conversational Language Understanding

Intents and utterances:
- Utterance: What is the time?; intent: GetTime
- Utterance: Turn the light on.; intent: TurnOnDevice
- Utterance: Will I need an umbrella tonight?; intent: GetWeather

1. In the Azure portal, deploy a Language Service to West Europe
2. Go to https://language.cognitive.azure.com/
3. Create a project 