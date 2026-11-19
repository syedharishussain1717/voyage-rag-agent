# VoyageAI -- Destination Intelligence & Cultural Travel Companion

**GitHub Repository:** https://github.com/syedharishussain1717/voyage-rag-agent
**Project:** VoyageAI -- Destination Intelligence & Cultural Travel
Companion\
**Selected document:** *VoyageAI Official Destination Guide Japan (Tokyo
& Kyoto)*\
**Submission date:** 19 November 2026

## 1. Document selected and reason

I selected a 20-page Japan destination guide covering Tokyo and Kyoto.
It contains practical travel information, including transportation,
landmarks, cultural etiquette, food, emergency contacts, currency,
seasons, accommodation, and visa-related guidance.

I chose this document because it provides a focused and useful knowledge
base for a travel assistant. Its range of topics makes it suitable for
testing document ingestion, retrieval, source-page citations, follow-up
questions, and the agent's ability to recognize when an answer is not
available in the document.

## 2. Project overview and implementation

VoyageAI is a retrieval-augmented generation (RAG) travel assistant
designed to answer questions using the selected Japan guide.

The PDF is loaded and split into smaller text chunks. The chunks are
converted into embeddings and stored in a persistent Chroma vector
database. When a user asks a document-related question, the agent
retrieves relevant passages and uses them to formulate an answer with
the source PDF page number.

The project uses LangChain's agent framework, a Groq-hosted language
model, Hugging Face sentence-transformer embeddings, Chroma for vector
storage, SQLite-backed conversation checkpoints, and Streamlit for the
user interface.

## 3. Extra tools added

In addition to document retrieval, I implemented travel utility tools:

-   **Currency conversion:** Converts amounts between supported
    currencies using illustrative reference rates. It clearly informs
    users that the rates are not live market rates.
-   **Travel budget estimation:** Estimates a Japan trip budget using
    the selected travel duration and travel style (budget, moderate, or
    luxury).

These tools extend the assistant beyond document question answering
while keeping their limitations explicit.

## 4. Ten test questions and results

The agent was evaluated using eight answerable questions and two
questions outside its available knowledge.

  ------------------------------------------------------------------------
                            \# Test question         Result
  ---------------------------- --------------------- ---------------------
                             1 What is the police    PASS
                               emergency number in   
                               Japan?                

                             2 What is the emergency PASS
                               number for fire and   
                               ambulance services in 
                               Japan?                

                             3 What is the official  PASS
                               currency of Japan?    

                             4 Is tipping expected   PASS
                               in Japan?             

                             5 What are the two      PASS
                               subway lines in       
                               Kyoto?                

                             6 Approximately how     PASS
                               long does the Nozomi  
                               Shinkansen take from  
                               Tokyo to Kyoto?       

                             7 What is Kaiseki       PASS
                               cuisine?              

                             8 Which seasons are     PASS
                               recommended for       
                               visiting Japan?       

                             9 What will the exact   PASS -- correctly
                               weather be in Tokyo   declined
                               on December 15, 2027? 

                            10 What is Toyota's      PASS -- correctly
                               current stock price?  declined
  ------------------------------------------------------------------------

**Evaluation summary:** 10 out of 10 tests passed (100% automated
evaluation score). The eight document-based tests checked expected facts
and page citations. The two out-of-scope tests checked whether the agent
declined to provide unavailable information.

The detailed evaluation output is saved in
`evaluation/evaluation_results.json`. The evaluation method and its
limitations are described in `evaluation_report.md`.

## 5. One limitation / failure scenario

The project does not include a live weather API. When asked to predict
the exact weather in Tokyo on 15 December 2027, the agent could not
provide a reliable forecast and correctly explained this limitation. It
did not fabricate weather information.

This is a limitation of the implemented project scope rather than a
failed evaluation test. The agent also declined to provide Toyota's
current stock price because no live financial-data tool is connected.

## 6. Conversation memory demonstration

VoyageAI uses SQLite-backed conversation checkpointing to retain context
within a conversation thread. In testing, the assistant remembered the
Japan travel context and the user's currency-conversion context in a
follow-up question, allowing the conversation to continue without
repeating the earlier details.

**Insert your screenshot below.** Capture the Streamlit conversation
showing the initial message that establishes the context and the
follow-up message where VoyageAI correctly uses that earlier context.

![VoyageAI conversation memory
demonstration](screenshots/memory_conversation.png)

*Figure 1. Screenshot demonstrating VoyageAI's conversational memory.
Add the screenshot at `screenshots/memory_conversation.png` before
submission.*

## 7. Conclusion

VoyageAI demonstrates a working document-grounded travel assistant with
PDF ingestion, text chunking, vector search, page-based citations,
additional travel utility tools, and conversational memory. It passed
all ten configured evaluation tests, including two tests designed to
verify that it does not invent answers to questions outside its
available knowledge.

The automated score is based on expected phrase and citation checks, so
it should not be interpreted as a guarantee that every generated detail
is semantically correct. Overall, the project meets its core objective
of providing a practical, document-grounded travel companion for Japan.
