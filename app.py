from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import requests
import json
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(
    page_title="Lead/Contact Enrichment from LinkedIn Profile",
    page_icon="✨"
)
st.title("Lead/Contact Enrichment from LinkedIn Profile ✨")
llm  = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3)
with st.form(key='link_form'):
    link = st.text_input("Add LinkedIn username url", placeholder="Type url", key='inputLink')
    sell = st.text_input("Add product to be sold", placeholder="Type product", key='inputPro')
    ins = st.text_input("Add instructions", placeholder="Type instructions", key='inputInst')
    submit_button3 = st.form_submit_button(label='Enter ➤')
if submit_button3 and link and sell and ins:
  
    url = "https://linkedin-data-scraper.p.rapidapi.com/person_deep"

    payload = { "link": link}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "dacc93bfecmsh336023176beccabp1fa929jsnbf31d1fec909",
        "X-RapidAPI-Host": "linkedin-data-scraper.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    link_dict = json.dumps(response.json())
    link_dict = str(link_dict)

    url2 = "https://linkedin-data-scraper.p.rapidapi.com/profile_updates"

    payload2 = {
        "profile_url": link,
        "posts": 1,
        "comments": 1,
        "reposts": 1
    }

    response_post = requests.post(url2, json=payload2, headers=headers)

    link_post = json.dumps(response_post.json())
    link_post = str(link_post)
    template_clear= """LinkedIn scrap: {linked}\n\n
    This is a linkedin scrap of a profile. Derive the following information from it and structure it neatly. If you cannot find particular information, say "Not specified". Don't make answers on your own.

    Output format:
    First name:
    \nLast name:
    \nPersonal email:
    \nLocation:
    \nCountry:
    \nCompany name (most recent):
    \nCompany domain: 
    \nProfessional email:
    \nMobile phone:
    \nJob title/role:
    \nSeniority:
    \nDepartment:
    \nEmail verified:
    \nEmail confidence:
    \nSMTP provider:
    \nDomain Age in days:
    """
    prompt_clear = ChatPromptTemplate.from_template(template_clear)
    chain_clear = LLMChain(llm=llm, prompt=prompt_clear)
    res_clear = chain_clear.invoke({"linked": link_dict})
    st.write("## Details:\n\n"+res_clear['text'])
    template= """LinkedIn scrap: {linked}\n\n
    You are an AI assistant that summarizes work history from LinkedIn profiles.
    Summarize this person's work history from their LinkedIn profile. List each company starting with the most recent and the roles they have had at those companies. After that write a paragraph summarizing their career progression/trajectory and call out anything that stands out like a major career change.
    Output should be under 2 headings: Current job and Previous experiences.
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = LLMChain(llm=llm, prompt=prompt)
    res = chain.invoke({"linked": link_dict})
    st.write("## Work history:\n\n"+res['text'])

    template1= """LinkedIn scrap: {linked}\n\n
    You are an AI assistant that extracts education details from LinkedIn profiles.
    Extract details on this person's education, including where they went to school and what they studied, from their LinkedIn profile. It should be in the following format:

    School Name 1 - Area of Study/Degree Earned

    School Name 2 - Area of Study/Degree Earned

    etc...
    """
    prompt1 = ChatPromptTemplate.from_template(template1)
    chain1 = LLMChain(llm=llm, prompt=prompt1)
    res1 = chain1.invoke({"linked": link_dict})
    st.write("## Education details:\n\n"+res1['text'])
    
    # Template 2
    template2 = """LinkedIn scrap: {linked}\n\n
    You are an AI assistant that extracts location information from LinkedIn profiles.
    Determine this person's current location based on their LinkedIn profile. Below their current location, list other places mentioned that they may have lived.
    """
    prompt2 = ChatPromptTemplate.from_template(template2)
    chain2 = LLMChain(llm=llm, prompt=prompt2)
    res2 = chain2.invoke({"linked": link_dict})
    st.write("## Locations:\n\n" + res2['text'])

    # Template 3
    template3 = """LinkedIn posts scrap: {linked}\n\n
    You are an AI assistant that summarizes recent LinkedIn posts from a profile. 
    Provide a detailed breakdown of any recent posts, comments or likes on this LinkedIn profile. Only talk about the posts and nothing else found in the profile. 
    """
    prompt3 = ChatPromptTemplate.from_template(template3)
    chain3 = LLMChain(llm=llm, prompt=prompt3)
    res3 = chain3.invoke({"linked": link_post[:5000]})
    st.write("## Summary of recent posts:\n\n" + res3['text'])

    # Template 4
    template4 = """LinkedIn scrap: {linked}\n\n
    You are an AI assistant that extracts personal details from LinkedIn profiles.
    Identify and summarize any personal details like hobbies, interests, or volunteering mentioned in this profile. Return this as a bulleted list.
    """
    prompt4 = ChatPromptTemplate.from_template(template4)
    chain4 = LLMChain(llm=llm, prompt=prompt4)
    res4 = chain4.invoke({"linked": link_dict})
    st.write("## Personal Interest/hobbies:\n\n" + res4['text'])

    # Template 5
    template5 = """LinkedIn scrap: {linked}\n\n
    You are an AI assistant that infers job responsibilities from LinkedIn profiles.
    Given this person's role and company, explain 5-10 key responsibilities they likely have in their job. Respond with this in a bulleted list.
    Output should be under 2 headings: Current job responsibilities and Past job responsibilities.
    """
    prompt5 = ChatPromptTemplate.from_template(template5)
    chain5 = LLMChain(llm=llm, prompt=prompt5)
    res5 = chain5.invoke({"linked": link_dict})
    st.write("## Job Resposibilities:\n\n" + res5['text'])

    # Template 6
    template6 = """LinkedIn scrap: {linked}\n\n
    You are an AI assistant that extracts technical skills and experience from LinkedIn profiles.
    Extract any key technologies, programming languages, frameworks, or tools that this person mentions experience with in their current and past jobs. Summarize these sections as separate paragraphs.
    """
    prompt6 = ChatPromptTemplate.from_template(template6)
    chain6 = LLMChain(llm=llm, prompt=prompt6)
    res6 = chain6.invoke({"linked": link_dict})
    st.write("## Technical Skills:\n\n" + res6['text']+"\n\n")

    # Template 7
    template7 = """
    Given the LinkedIn profile information for this person:

    Work History: {work}

    \nEducation Details: {ed}

    \nLocation: {loc}

    \nRecent Posts: {post}

    \nPersonal Details: {dets}

    \nJob Responsibilities: {job}

    \nTechnical Skills: {tech}

    \nYou are an AI assistant that recommends use cases based on a person's LinkedIn profile.
    Hypothesize 5 ways this person could use {prod}.
    """
    prompt7 = ChatPromptTemplate.from_template(template7)
    chain7 = LLMChain(llm=llm, prompt=prompt7)
    res7 = chain7.invoke({"work": res['text'], "ed":res1['text'], "loc":res2['text'], "post":res3['text'], "dets":res4['text'], "job":res5['text'], "tech":res6['text'], "prod":sell})
    st.write("## Use Cases:\n\n"+res7['text']+"\n\n")

    # Template 8
    template8 = """
    Given the LinkedIn profile information for this person:

    Work History: {work}

    \nEducation Details: {ed}

    \nLocation: {loc}

    \nRecent Posts: {post}

    \nPersonal Details: {dets}

    \nJob Responsibilities: {job}

    \nTechnical Skills: {tech}

    \nUse Cases of product to be sold to LinkedIn user: {use}

    You are an AI assistant that obeys instructions. 
    Product to be sold to the LinkedIn user: {prod}
    You will be given a task or a set of instructions to sell the product to the LinkedIn user. Use the above information to execute it. Write subjective to the LinkedIn user's current job, while taking some essense from his past experiences.
    \nTask/Instructions: {ins}
    """
    prompt8 = ChatPromptTemplate.from_template(template8)
    chain8 = LLMChain(llm=llm, prompt=prompt8)
    res8 = chain8.invoke({"work": res['text'], "ed":res1['text'], "loc":res2['text'], "post":res3['text'], "dets":res4['text'], "job":res5['text'], "tech":res6['text'], "prod":sell, "use": res7['text'],"ins":ins})
    st.write("## Final Output: "+res8['text'])
