Feature: Read record data

    Operator wants to test API service
    Input JSON is converted to base64 for example {"query":{"content":{"ID": "MCTS31"}}} => eyJxdWVyeSI6eyJjb250ZW50Ijp7IklEIjogIk1DVFMzMSJ9fX0= (converted in https://gchq.github.io/CyberChef/)

    Scenario Outline: Record received or not received
        Given API input object is "<input>", API endpoint is "<endpoint>" and method used is "<method>"
        When I ask to receive a record
        Then I should get a record "<answer>"

        Examples:
            |   input                                                   | endpoint                                             |   answer  | method |
            |   eyJxdWVyeSI6eyJjb250ZW50Ijp7IklEIjogIk1DVFMzMSJ9fX0=    | https://gdb.er4.ext.egovstack.net/data/mcts/1.1/read |   200     | post   |
            |   eyJxdWVyeSI6eyJjb250ZW50Ijp7IklEIjogImJsYWJsYSJ9fX0=    | https://gdb.er4.ext.egovstack.net/data/mcts/1.1/read |   404     | post   |
            |   eyJxdWVyeSI6eyJjb250ZW50Ijp7IklEIjogIjEyMzQ1In19fQ==    | https://gdb.er4.ext.egovstack.net/data/mcts/1.1/read |   404     | post   |
