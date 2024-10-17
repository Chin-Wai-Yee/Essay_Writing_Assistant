from File_handling import read_file_content
import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="Essay Suggestion", page_icon="💡")

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_openai_connection, get_collection

st.write("# Get Essay Suggestions 💡")

uploaded_file = st.file_uploader("Upload your essay", type=[
                                 "txt", "doc", "docx", "pdf"])


def get_essay_suggestions(essay, userinfo):

    client = get_openai_connection()

    system_prompt = """ You will be given an essay and the weaknesses and strengths of a student
                      in writting an essay. Provide the score of the essay. Then give some
                      suggestion or improvement on the essay based on the weaknesses and
                      strengths of the student. You can change some word or sentence of the
                      essay to improve it.

                      The prompt should be in this format:

                      Type of Essay:
                      Content: ?/10
                      Organization: ?/10
                      Clarity and Coherence: ?/10
                      Grammar and Language: ?/10
                      Evidence and Support: ?/10
                      Conclusion: ?/10
                      Overall Score: ?/10

                      1.
                      Original Text:
                      Suggestion:
                      Improved Version:
                      2.
                      Original Text:
                      Suggestion:
                      Improved Version:
                      3.
                      Original Text:
                      Suggestion:
                      Improved Version:
                      """

    sample_essay = """
  Having a healthy lifestyle is all about choosing to live your life in the most healthy way possible. There are a few things you have to do to start living your life in this way, i.e., the healthy way. This means doing some amount of exercise daily, such as jogging, yoga, playing sports, etc. Adding to this, you must also have a balanced and nutritional diet with all the food groups. It would be best if you were taking the right amount of proteins, carbohydrates, vitamins, minerals, and fats to help you have a proper diet. Grouped with these two essential aspects (diet and exercise), a healthy person also maintains the same sleep cycle, which should consist of around 7-8 hours of sleep.
However, we must remember that a healthy lifestyle not only refers to our physical and mental health. Maintaining a balanced diet, exercising daily, and sleeping well are essential parts of a healthy lifestyle. But feeling happy is also a big part of a healthy lifestyle. To enable happiness, thinking positively is a must. When a person does not feel happy or good about themselves, they are not entirely healthy. Thus we must do our best to think positively so that we can feel happy rather than sad.
We have talked about what all entails a healthy life, so now we must speak of what all does not. There are several things that one must avoid in order to live a healthy lifestyle. These include the kind of practices and habits that are harmful to us and also to the people around us, i.e., society. Such practices and habits include gambling, smoking, drinking, illegal drugs, or any other things that can turn into an addiction. These habits are harmful to not only you but for all the people around you, as addiction causes unhealthy attitudes and behaviors. Other unhealthy practices include skipping meals and eating junk food.
The benefits of a healthy lifestyle are manifold: living a healthy life allows you to live longer, which means that you get to spend more time with your family. Exercising daily will enable you to release endorphins and helps you feel happier. Regular exercise also improves the health of your skin and hair, bettering your appearance as well. Healthy lifestyles also primarily reduce your risk of life-threatening diseases such as cancer, diabetes, etc. and also reduce your susceptibility to cardiac arrests.
Overall, living your life in a healthy way only has benefits, and that’s why it is recommended that you do everything you can to have a healthy lifestyle. So, eat three nutritional meals a day, avoid unhealthy junk food, go for a run or jog in the morning, get your full 8 hours of sleep, and avoid bad habits like drugs, alcohol, and smoking. A healthy lifestyle is the best thing that you can do to your body, and you will be thanking yourself for following a healthy lifestyle in the later years of your life.
"""
    sample_userinfo = """
Strengths : Clear Message, Well-Organized, Comprehensive Content, Encouraging Tone, Use of Specific Examples. Weaknesses : Repetition, Vague Assertions, Lack of Evidence, Generalized Conclusion, Sentence Structure, Transitions and Flow.
"""
    sample_answer = """
Based on the strengths and weaknesses of the essay, I would score it in different categories as follows:

Content: 7/10
- The essay provides a good overview of the topic and covers key elements such as diet, exercise, and mental health. However, some points are repeated, and more depth could be provided, particularly on the mental health aspect. The essay would benefit from further elaboration on strategies to maintain a healthy lifestyle and evidence-based claims.

Organization: 8/10
- The essay follows a logical structure, starting with what constitutes a healthy lifestyle and progressing to unhealthy habits to avoid. However, transitions between sections could be smoother, and the conclusion could offer a more impactful reflection or call to action instead of repeating earlier points.

Clarity and Coherence: 7/10
- The essay is clear and easy to follow, but some sentences are overly long or repetitive. Breaking down complex ideas into shorter sentences and avoiding redundancy would improve clarity. The flow of ideas can also be enhanced with better transitions.

Grammar and Language: 8/10
- Overall, the grammar is solid, and the language is understandable. However, there are a few instances where sentence structures could be improved for readability and better expression of ideas.

Evidence and Support: 6/10
- The essay lacks concrete evidence to support some claims. For example, the link between exercise and skin health or the impact of positive thinking on overall well-being could be backed by research or studies, which would improve the essay’s credibility.

Conclusion: 7/10
- The conclusion ties everything together but feels somewhat repetitive. A stronger, more engaging conclusion could provide new insights or an inspirational call to action to make the essay more memorable.

Overall Score: 7/10
- The essay is good, with a clear message and sound structure, but it could benefit from more specific examples, evidence, and smoother transitions. Making these improvements would make it more persuasive and polished.


Here are some specific suggestions to improve your essay, based on the analysis. I’ll provide the original text along with solutions for each point of improvement:

1. Repetition of Ideas
Original Text:
"There are a few things you have to do to start living your life in this way, i.e., the healthy way. This means doing some amount of exercise daily, such as jogging, yoga, playing sports, etc. Adding to this, you must also have a balanced and nutritional diet with all the food groups."

Suggestion: This idea of exercise and balanced diet is repeated multiple times throughout the essay. You can condense this section by combining it with another and focusing on the benefits to reduce repetition.

Improved Version:
"A healthy lifestyle starts with daily physical activity, like jogging, yoga, or playing sports, and maintaining a balanced, nutritious diet that includes all essential food groups such as proteins, carbohydrates, vitamins, and fats."

2. Vague Assertions
Original Text:
"But feeling happy is also a big part of a healthy lifestyle. To enable happiness, thinking positively is a must. When a person does not feel happy or good about themselves, they are not entirely healthy."

Suggestion: Instead of stating this in a general way, you could provide more practical advice on how people can cultivate positive thinking and happiness as part of their healthy lifestyle.

Improved Version:
"Mental well-being is equally important in a healthy lifestyle. Practices like mindfulness, meditation, and gratitude can help cultivate positive thinking. When you maintain a positive mindset, it improves your overall health by reducing stress and enhancing emotional resilience."

3. Lack of Evidence
Original Text:
"Regular exercise also improves the health of your skin and hair, bettering your appearance as well."

Suggestion: This claim would benefit from being backed by evidence, such as a reference to studies or research. If you're not adding a citation, you can adjust the statement to sound less assertive.

Improved Version:
"Regular exercise is known to boost circulation and promote skin health, which can contribute to a healthier appearance."
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Essay: {sample_essay}\nUserInfo: {sample_userinfo}\n\nPlease provide specific suggestions on how to improve the essay based on the provided user information."},
            {"role": "assistant", "content": sample_answer},
            {"role": "user", "content": f"Essay: {essay}\nUserInfo: {userinfo}\n\nPlease provide specific suggestions on how to improve the essay based on the provided user information."}
        ]
    )

    return response.choices[0].message.content

# Function to add the reponse to collection
def add_to_collection(response):
    collection = get_collection("user_performance")
    collection.insert_one(response)

if uploaded_file:
    essay_content, file_type = read_file_content(uploaded_file)
    if file_type == "unsupported":
        st.write("Unsupported file type")
        st.stop()

    with st.expander("Uploaded Essay:"):
        st.markdown(essay_content)

    if st.button("Get Suggestions"):
        # Here you would typically use an AI model or API to generate suggestions
        # For this example, we'll just provide some generic feedback
        suggestions = ""
        with st.spinner("Generating suggestions..."):
            suggestions = get_essay_suggestions(
                essay_content, "Wring style: Analytical, Vocabulary level: Advanced, Sentence complexity: Moderate, Common themes: Technology, Social issues")

        st.write("Suggestions:")
        st.markdown(suggestions)
        data = {
            "timestamp": datetime.now(),
            "user_id": "2103370",
            "comments": suggestions,
            "score": 7,
        }

        add_to_collection(data)