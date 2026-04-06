Feature: Graph RAG chatbot behavior

  Background:
    Given a running Neo4j graph with indexed document chunks
    And the backend is configured with Hugging Face inference
    And the frontend is connected to the backend API

  Scenario: Answer a question with matched documents
    When the user asks "How does our model evaluation pipeline work?"
    Then the chatbot returns a grounded answer
    And the response includes matched document references
    And each reference maps to a known source document

  Scenario: Handle unknown context safely
    When the user asks a question outside the indexed knowledge
    Then the chatbot states uncertainty explicitly
    And no fabricated citation is returned

  Scenario: Evaluation tab displays retrieval metrics
    When the user opens the Evaluation tab
    Then retrieval quality metrics are displayed
    And generation quality metrics are displayed
    And end-to-end latency metrics are displayed
