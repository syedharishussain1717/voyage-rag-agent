# VoyageAI -- Evaluation Report

**Project:** VoyageAI -- Destination Intelligence & Cultural Travel
Companion\
**Evaluation date:** 19 November 2026\
**Document used:** *VoyageAI Official Destination Guide Japan (Tokyo &
Kyoto)*\
**Evaluation script:** `evaluation/test_eval.py`\
**Detailed results:** `evaluation/evaluation_results.json`

## 1. Evaluation objective

The purpose of this evaluation was to assess whether VoyageAI can
retrieve relevant information from its uploaded Japan destination guide,
provide answers with page references, and appropriately decline
questions that cannot be answered using its available knowledge.

## 2. Evaluation method

Ten questions were tested:

-   Eight questions were answerable from the destination guide.
-   Two questions required information outside the guide and the agent's
    available tools.
-   For answerable questions, the evaluation script checked expected
    facts and at least one expected page citation.
-   For unanswerable questions, it checked whether the agent
    appropriately indicated that it could not provide the requested
    information.

The evaluation script uses expected-phrase and citation checks.
Therefore, its score is an automated screening result; it does not
independently verify every sentence or establish perfect semantic
accuracy.

## 3. Test cases and results

  ------------------------------------------------------------------------
                     \# Test question    Expected result  Result
  --------------------- ---------------- ---------------- ----------------
                      1 What is the      110; page 11     PASS
                        police emergency citation         
                        number in Japan?                  

                      2 What is the      119; page 11     PASS
                        emergency number citation         
                        for fire and                      
                        ambulance                         
                        services in                       
                        Japan?                            

                      3 What is the      Japanese Yen     PASS
                        official         (JPY); relevant  
                        currency of      page citation    
                        Japan?                            

                      4 Is tipping       Explain that     PASS
                        expected in      tipping is not   
                        Japan?           practiced or     
                                         expected;        
                                         relevant page    
                                         citation         

                      5 What are the two Karasuma and     PASS
                        subway lines in  Tozai; page 3    
                        Kyoto?           citation         

                      6 Approximately    Approximately 2  PASS
                        how long does    hours 15         
                        the Nozomi       minutes;         
                        Shinkansen take  relevant page    
                        from Tokyo to    citation         
                        Kyoto?                            

                      7 What is Kaiseki  Identify it as a PASS
                        cuisine?         traditional      
                                         multi-course     
                                         dining style;    
                                         relevant page    
                                         citation         

                      8 Which seasons    Spring and       PASS
                        are recommended  autumn; relevant 
                        for visiting     page citation    
                        Japan?                            

                      9 What will the    State that an    PASS
                        exact weather be exact future     
                        in Tokyo on      forecast is      
                        December 15,     unavailable      
                        2027?                             

                     10 What is Toyota's State that       PASS
                        current stock    real-time stock  
                        price?           information is   
                                         unavailable      
  ------------------------------------------------------------------------

## 4. Evaluation summary

  Metric                           Result
  ---------------------------- ----------
  Total questions                      10
  Answerable questions                  8
  Unanswerable questions                2
  Passed                               10
  Failed                                0
  Automated evaluation score     **100%**

The detailed answers and per-test results are stored in
`evaluation/evaluation_results.json`.

## 5. Limitation / failure scenario explained

One limitation tested was the request for the exact weather in Tokyo on
15 December 2027. The destination guide contains general seasonal travel
information, but VoyageAI does not have a live weather service or a
reliable forecast for that specific future date. The agent correctly
explained that it could not provide the exact forecast rather than
inventing weather conditions.

The Toyota stock-price question demonstrated a similar boundary: the
project does not include a live financial-data tool. These are scope
limitations rather than failed test cases. Both questions were correctly
handled as unanswerable, so they passed the refusal checks.

## 6. Conclusion

VoyageAI passed all ten configured test cases. The results indicate that
the agent can answer the selected guide-based questions with relevant
page citations and can decline the two tested requests that fall outside
its available information and tools. The 100% score should be
interpreted in the context of the lightweight automated checks described
above, with manual review remaining important for factual accuracy and
citation quality.
