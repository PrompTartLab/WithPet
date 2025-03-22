# 🐾 WithPet: Pet-Friendly Places Finder Chatbot 🐾

## 📌 Project Overview

**WithPet** is a chatbot that helps users **find pet-friendly facilities** with ease. It provides a comprehensive database of locations where pets are allowed, enabling users to search for places based on location, category, operating hours, parking availability, and pet-related amenities.

## 🚀 Features

- Search for pet-friendly facilities by **location** (city, district).
- Filter by **category** (e.g., cafes, restaurants, pet hospitals, etc.).
- Check **operating hours**, including weekends and holidays.
- Identify whether **parking** is available.
- Get details about **pet size restrictions**, **additional pet charges**, and **indoor/outdoor pet access**.
- Retrieve **contact details** including phone number and website.

## 💡 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, LangChain, LangGraph
- **LLM**: OpenAI GPT-4o (API)
- **Database**: FAISS (Vector Store), SQLite (In-memory)

## 🛠️ Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/PrompTartLab/WithPet.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Streamlit Secrets (secrets.toml):
   ```shell
   PROJECT_DIR="{project_dir}"
   CONNECTED_DIR="{connected_dir}"
   OPENAI_API_KEY="{openai_api_key}"
   LANGSMITH_API_KEY="{langsmith_api_key}"
   PINECONE_API_KEY="{pinecone_api_key}"
   PINECONE_INDEX_NAME="{pinecone_index_name}"
   ```
   - project_dir: Full path to the project directory (e.g., /home/ubuntu/WithPet).
   - connected_dir: Directory for data and FAISS storage (e.g., /home/ubuntu/WithPet).
4. Start the application:
   ```bash
   streamlit run home.py
   ```

## 🎯 How to Use

![withpet](withpet.gif)

### 1. Ask Questions in Natural Language

- Simply type your query in the chatbot’s text input box.

> Example: "Find a pet-friendly pension in Incheon without additional pet fees."

- All results **automatically include pet-friendly places**, so you **don’t need to specify** “pet-friendly” in your query.

### 2. Use Sidebar Filters

- Select **Region / Type / Options** from the left sidebar and click **검색하기 button** to auto-generate a question.
- Currently, only metropolitan cities (특별시, 광역시) are selectable in the sidebar.
- For more detailed queries, type them directly into the chatbot!

## 🔎 Workflow

![image](https://github.com/user-attachments/assets/43e5f4d6-7157-4d7c-b3d0-b643a6afeebc)

✅ **LangGraph-based Workflow**

- Uses **LangGraph** to interpret user queries and execute appropriate search processes.

✅ **Text-to-SQL Approach**

- Traditional RAG-based methods rely on **vector embedding** for similarity searches. However, since this project uses **boolean and categorical columns**, the RAG approach was not optimal.
- Instead, the **LLM dynamically generates SQL queries** to filter results.

> Example Query: "Recommend a pet-friendly café in Seoul with parking."
>
> → The system retrieves locations where **`city = 'Seoul'`** and **`parking_available = 'Y'`**.

✅ **Few-shot Learning for SQL Generation**

- To improve SQL generation accuracy, **predefined question-SQL pairs** are embedded in a vector store.
- The model retrieves **similar examples** for reference when generating queries.

✅ **Error Handling**

- The chatbot ignores queries unrelated to **pet-friendly places** to maintain relevance.

## 📌 Acknowledgment

This project utilizes the **"Pet-Friendly Cultural Facility Location Data"** provided by the **한국문화정보원(KCISA)** through the [Culture Big Data Platform](https://www.bigdata-culture.kr/bigdata/user/main.do) under the Open License Type 1. The original dataset is **freely available** at [Culture Big Data Platform](https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=3c3d50c0-0337-11ee-a67e-69239d37dfae).

## 📞 Contact

For any inquiries or issues, please reach out to [**jiyoon0424@gmail.com**](mailto:jiyoon0424@gmail.com) or open an issue on GitHub.
