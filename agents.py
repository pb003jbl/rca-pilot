import dspy as ds
import time as t


# Define Agents
class GeneralAssistant(ds.Signature):
        """ You're a helpful assistant whose work scope is limited to answer general queries regarding Root Cause Analysis on any data.
        You're capable of answering any general query in your scope or creating reports on any topic in your scope.
        Rules : 
        1. If the user query : {goal} doesn't match your scope, ask the user politely to ask something which is in your work scope & suggest couple of examples what user can ask.
        2. If the user query doesn't contain an Incident number (example : INCxxxxxx), Ask user to specify Incident number with the query.
        [Output formatting : Mark down Text]
        """
        dataset = ds.InputField(desc="Provided dataset")
        goal = ds.InputField(desc="User specified query or task or goal")
        answer = ds.OutputField(desc="Answer to the user query")

        # decision = ds.OutputField(desc="""Take a decision if other agents are required to answer the following query :{goal}
        #              Response format : boolean ['true' if other agents are required, else 'false']""")

class ResearchAnalyst(ds.Signature):
        """You're a Research analyst Agent, expert in Root cause analysis & research on any given dataset.
          Identify the root cause of the issue and provide a step-by-step analysis of the contributing factors.
          Offer recommendations for addressing the root cause and preventing future occurrences: 

          Dataset Summary: [The dataset is an Incident Management System (IMS) data containing 16 rows and 17 columns. 
          The incidents are identified by their unique numbers (INCxxxxxx). 
          The priority of each incident is categorized as 'High' (2) and the affected country is not specified in the dataset. 
          The 'Assignment Group' column indicates the Oracle AMS group responsible for resolving the incidents. 
          The 'Opened' column shows the date and time when the incident was reported, while the 'Closed' column indicates 
          the date and time when the incident was resolved. 
          The 'EBS Resolution' column provides information about the type of resolution, such as 
          'Trouble Shoot', 'AdHoc Reporting', 'Performance/Sys Admin', 'Transaction Processing', etc. 
          The 'Close notes' column contains additional information about the incident resolution.]
          """
        dataset = ds.InputField(desc="Uploaded dataset for analysis on user specified goal : {goal}.")
        goal = ds.InputField(desc="User specified query or task or goal")
        rca:str = ds.OutputField(desc="Detailed Research")       


class Editor(ds.Signature):
        """You're an Report Editor Agent which is suppose to generate a detailed report based on the user query:{goal} & context :{rca}.
          Analyze the information in all the rows & create a detailed report on root cause analysis on this dataset.
          Report must contains the following -
        
        Introduction: Outlines the purpose of the report, the intended audience, and the scope of the document.
        Problem Description: Provides a clear and detailed description of the problematic event, including the date of occurrence, the involved person or team who detected the event, the affected parties, and the extent of the effects.
        Timeline of Events: Captures and describes all the events that led to the event at fault and the ones that followed it, including the timing of each event and the involved parties.
        Utilized Methods: Details the analysis methodologies used to determine the root cause, the people involved at each step of the process, and their specific roles.
        Findings Explanation: Captures and reports all findings, no matter how small, to help further investigate cause-and-effect relationships and prevent the rise of potential problems.
        Recommendations: Lists solutions to the problem that can help prevent the issue from occurring again, including specific, actionable steps the business can take to minimize or eliminate the root cause of the problem.
          
        [Output formatting : Markdown Text]
        """
        rca = ds.InputField(desc="Root cause analysis")
        goal = ds.InputField(desc="User specified query or task or goal")
        report:str = ds.OutputField(desc="markdown-formatted section")      


# Configure the language model

lm = ds.LM(model='mistral/open-mistral-7b',max_tokens = 2048, api_key='QEhd2LOvC1OsJm5BYlj0wfjP89VMj9iK')
if not ds.settings.configure:
    ds.settings.configure(lm=lm)
else:ds.settings.configure(lm=lm)
master_dataset = []


genbot = ds.ChainOfThought(GeneralAssistant)
analyst = ds.ChainOfThought(ResearchAnalyst)
editor = ds.ChainOfThought(Editor)


# editor(rca=analyst(dataset=master_dataset))
# genbot(dataset=master_dataset,goal="{prompt}")

agents:dict={}
# o_analyst = analyst(dataset=master_dataset)
# o_editor = editor(rca=o_analyst.rca)
# o_genai = genbot(dataset=master_dataset,goal="{prompt}")


def invokeEditor(prompt):
    agents.update(editor(rca=analyst(dataset=master_dataset,goal=prompt),goal=prompt))
    # t.sleep(5)
    # print(agents)
    return agents

def invokeAssistant(prompt):
    # o_genai = genbot(dataset=master_dataset,goal=prompt)
    agents.update(genbot(dataset=master_dataset,goal=prompt))
    # t.sleep(5)
    # print(agents)
    return agents

