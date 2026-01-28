from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter # <--- Added Import
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough





def build_knowledge_base(md_path, json_path):
    documents = []

    # --- A. Load & Split Markdown (Concepts) ---
    with open(md_path, "r") as f:
        md_text = f.read()

    # Step 1: Structural Split (Keep sections together)
    headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]
    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    header_splits = md_splitter.split_text(md_text)

    # Step 2: Optimization Split (Chunking & Overlap)
    # This ensures large sections are broken down into digestible pieces for the LLM
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,    # Target size (characters)
        chunk_overlap=100   # Overlap to preserve context at boundaries
    )

    # Split the header-based documents further
    final_md_splits = text_splitter.split_documents(header_splits)
    documents.extend(final_md_splits)

    # --- B. Load JSON (Variables) ---
    # JSON objects are usually atomic (definitions), so we rarely chunk them further.
    # The loader treats each object in the list as one document.
    print(f"Loading JSON: {json_path}")
    loader = JSONLoader(
        file_path=json_path,
        jq_schema='.[]',
        text_content=False
    )
    json_splits = loader.load()
    documents.extend(json_splits)

    # print(f"Total Chunks Created: {len(documents)}")

    # --- C. Create Vector Store ---
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        collection_name="groq_rag_test"
    )

    return vectorstore.as_retriever(search_kwargs={"k": 2}
)







