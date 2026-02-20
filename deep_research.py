import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

def enrichQuery(query: str, question1: str, question2: str, question3: str, answer1: str, answer2: str, answer3: str):
    enriched_query = f"""
        Main Topic:
        {query}
        Clarifications:
        Q1: {question1}
        A1: {answer1}
        Q2: {question2}
        A2: {answer2}
        Q3: {question3}
        A3: {answer3}
    """

    return enriched_query

async def run_full(
    query: str,
    question1: str,
    question2: str,
    question3: str,
    answer1: str,
    answer2: str,
    answer3: str,
):
    enriched_query = enrichQuery(query, question1, question2, question3, answer1, answer2, answer3)

    async for chunk in ResearchManager().run_full(enriched_query):
        yield chunk

async def run_questions_generation(query: str):
    questions = await ResearchManager().run(query)
    q1_text = questions.questions[0].question
    q2_text = questions.questions[1].question
    q3_text = questions.questions[2].question
    print(questions)
    return (
        query,    
        q1_text,
        q2_text,
        q3_text,                  
        gr.update(visible=True),    # show followup form
        gr.update(visible=True),    # hide first input section
        gr.update(label=q1_text, value="", interactive=True),
        gr.update(label=q2_text, value="", interactive=True),
        gr.update(label=q3_text, value="", interactive=True),
    )

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")

    stored_query = gr.State()
    stored_q1 = gr.State()
    stored_q2 = gr.State()
    stored_q3 = gr.State()

    with gr.Column() as first_section:
        query_textbox = gr.Textbox(label="What topic would you like to research?")
        run_button = gr.Button("Run", variant="primary")
    
    with gr.Column(visible=False) as followup_section:
        gr.Markdown("### Please answer a few clarifying questions")

        q1 = gr.Textbox(label="")
        q2 = gr.Textbox(label="q2")
        q3 = gr.Textbox(label="q3")

        regenerate_button = gr.Button("Regenerate Questions", variant="primary", scale=0)
        continue_button = gr.Button("Continue", variant="primary")

    report = gr.Markdown(label="Report")
    
    run_button.click(
        fn=run_questions_generation,
        inputs=query_textbox,
        outputs=[stored_query, stored_q1, stored_q2, stored_q3, followup_section, first_section, q1, q2, q3,],
    )
    query_textbox.submit(
        fn=run_questions_generation,
        inputs=query_textbox,
        outputs=[stored_query, stored_q1, stored_q2, stored_q3, followup_section, first_section, q1, q2, q3,],
    )
    
    #run_button.click(fn=run, inputs=query_textbox, outputs=report)
    #query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)
    continue_button.click(
    fn=run_full,
    inputs=[
        stored_query,   # query
        stored_q1,      # question1
        stored_q2,      # question2
        stored_q3,      # question3
        q1,             # answer1
        q2,             # answer2
        q3,             # answer3
    ],
    outputs=report,
    )

    regenerate_button.click(
        fn=run_questions_generation,
        inputs=query_textbox,
        outputs=[stored_query, stored_q1, stored_q2, stored_q3, followup_section, first_section, q1, q2, q3,],
    )

    
ui.launch(inbrowser=True)

