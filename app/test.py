from backend import ESG_Bot
from langchain.document_loaders import PyPDFLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os 
from dotenv import load_dotenv 
import openai

load_dotenv("/Users/nicoleyap/Documents/GitHub/esg-chatbot-demo/app/.env", override=True)
# llm = AzureChatOpenAI(
#     azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
#     api_key=os.environ['AZURE_OPENAI_APIKEY'],
#     deployment_name=os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'],
#     model_name=os.environ['AZURE_OPENAI_MODEL_NAME'],
#     api_version=os.environ['AZURE_OPENAI_API_VERSION'],
#     temperature=0,
#     max_tokens=700,
#     timeout=None,
#     max_retries=2,
# )

from azure.search.documents.indexes.models import (
    ScoringProfile,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    TextWeights,
)


doc_path="short-ghg-calc.pdf"
doc_info = PyPDFLoader(doc_path)
doc_info_load = doc_info.load()

embeddings = AzureOpenAIEmbeddings(azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'], 
                                   api_key=os.environ['AZURE_OPENAI_APIKEY'], 
                                   model=os.environ['TEXT_EMBEDDING_MODEL_NAME'],
                                   azure_deployment=os.environ['TEXT_EMBEDDING_DEPLOYMENT_NAME'])
endpoint = os.environ['AZURE_AI_SEARCH_ENDPOINT']
admin_key = os.environ['AZURE_AI_SEARCH_API_KEY']
index = os.environ['AZURE_AI_SEARCH_INDEX']

print("length", len(embeddings.embed_query("Text")))
fields = [
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
        filterable=True,
    ),
    SearchableField(
        name="content",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=len(embeddings.embed_query("Text")),
        vector_search_profile_name="myHnswProfile",
    ),
    SearchableField(
        name="metadata",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
]


azure_search = AzureSearch(
              azure_search_endpoint=endpoint,
              azure_search_key=admin_key,
              index_name=index,
              embedding_function=embeddings.embed_query,
              semantic_configuration_name="default",
              fields=fields
          )


# print(doc_info_load)
print("adding docs into azure search")
response = azure_search.add_documents(documents=doc_info_load)

# azure_search.add_documents(documents=doc_info_load)

print("Added document into Azure Search")

# search_results = azure_search.search(
#     query="Tell me more about GHG",
#     k=3,
#     search_type="similarity"
#   )


# print("page_content", search_results[0].page_content)

# print(llm.invoke([{"role": "user", "content": "Tell me more about ESG"}]))
# bot = ESG_Bot()
# resp = bot.get_response("Tell me more about GHG")
# print(resp)