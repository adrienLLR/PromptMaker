# The Prompt Maker

LLMs are great tools to assist us in a wide variety of tasks. But they lack some reasoning mechanisms that we humans possess and that are essential
to produce coherent and valid answers : Self-Reflection, Back Tracking, Breaking the problem into smaller problems.\
    

To address that, the Prompt Maker allows you to construct a chain of prompts where you can re-utilize or not the output of the previous prompt.
Therefore, you can implement the reasoning mechanisms enumerated before :
- Self-Reflection : Ask the LLM to ponder about the previous output
- Back Tracking : Ask the LLM to modify the previous output to better suit the previous prompt
- Breaking the problem into sub-problems : Make the LLM perform several tasks, then combine everything at the end


![](img/illustration.png)