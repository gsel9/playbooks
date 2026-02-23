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