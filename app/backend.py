from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai.embeddings import AzureOpenAIEmbeddings
# from langchain.document_loaders import PyPDFLoader
# from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage


import os


# LLM_RAG
class ESG_Bot:
  def __init__(self):
    load_dotenv(".env", override=True)
    self.llm = AzureChatOpenAI(
      azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
      api_key=os.environ['AZURE_OPENAI_APIKEY'],
      deployment_name=os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'],
      model_name=os.environ['AZURE_OPENAI_MODEL_NAME'],
      api_version=os.environ['AZURE_OPENAI_API_VERSION'],
      temperature=0,
      max_tokens=700,
      timeout=None,
      max_retries=2,
    )

    self.embeddings = AzureOpenAIEmbeddings(azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'], 
                                   api_key=os.environ['TEXT_EMBEDDING_APIKEY'], 
                                   model=os.environ['TEXT_EMBEDDING_MODEL_NAME'],
                                   azure_deployment=os.environ['TEXT_EMBEDDING_DEPLOYMENT_NAME'])


    endpoint = os.environ['AZURE_AI_SEARCH_ENDPOINT']
    admin_key = os.environ['AZURE_AI_SEARCH_API_KEY']
    index = os.environ['AZURE_AI_SEARCH_INDEX']

    self.azure_search = AzureSearch(
              azure_search_endpoint=endpoint,
              azure_search_key=admin_key,
              index_name=index,
              embedding_function=self.embeddings.embed_query,
              semantic_configuration_name="default"
          )

  def get_response(self, query):
    # search_results = self.client.hybrid_search(
    #   search_text=query,
    #   top=5,
    # )
    search_results = self.azure_search.search(
      query=query,
      k=3,
      search_type="similarity"
    )

    # print(search_results)
    sources_formatted = search_results[0].page_content
    GROUNDED_PROMPT="""
    You are an Environmental, Social and Governance (ESG) Information Assistant for 
    companies who need some direction on ESG related information in Singapore
    Answer with the facts listed in the list of sources below.
    If there isn't enough information below, you may generate base on your knowledge
    If you are not sure, say Sorry you don't have enough information to know.
    Keep the answer precise.
    Do not generate answers that are not relevant to ESG.
    Query: {query}
    Sources:\n{sources}
    """

    system_message = SystemMessage(content=GROUNDED_PROMPT.format(query=query, sources=sources_formatted))
    # user_message = HumanMessage(content=query)

    # Invoke the LLM with the messages
    response = self.llm.invoke([system_message])
    
    # Print and return the response content
    # print(response.content)
    print(response.content)
    return response.content

  # def add_doc(self, doc_path, type="pdf"):
  #   if type == "pdf":
  #     doc_info = PyPDFLoader(doc_path)
  #     doc_info_load = doc_info.load()

    # elif type == "docs":
    #   doc_info = Docx2txtLoader(doc_path)
    #   doc_info_load = doc_info.load()
    #   splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap=200)
    #   chunks = splitter.split_documents(doc_info_load)
    #   doc_info_load = chunks
    
    #self.azure_search.add_documents(doc_info_load)
    
    
  def delete_doc(self, index):
    """
    # TODO: delete documents
    """
    return 


