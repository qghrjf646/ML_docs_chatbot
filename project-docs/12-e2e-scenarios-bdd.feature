Feature: Graph RAG assistant quality and grounding

  Scenario: Grounded response with evidence
    Given documents are ingested into the graph
    When a user asks a domain question
    Then the answer is provided
    And matched documents are included
    And all citations resolve to existing graph-linked chunks

  Scenario: Unknown-answer behavior
    Given the question is outside indexed knowledge
    When the chatbot responds
    Then it states uncertainty
    And it does not fabricate citations

  Scenario: Evaluation transparency
    Given benchmark runs are available
    When the user opens evaluation tabs
    Then retrieval, generation, and end-to-end metrics are visible
