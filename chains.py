from langchain.prompts import PromptTemplate
import logging

logging.basicConfig(level=logging.INFO)

def generate_blog(llm, blog_topic, word_limit, blog_style, tone):
    if not blog_topic:
        raise ValueError("Please provide a valid blog topic and ensure word_limit is at least 500 words.")
    try:
        prompt = PromptTemplate.from_template(
            """
            ### BLOG TOPIC:
            {blog_topic}
            
            ### INSTRUCTIONS:
            Write a blog post on the topic "{blog_topic}" that is at least {word_limit} words long. 
            The blog should be in the {blog_style} style and written in a {tone} tone. 
            The content should be broken down into multiple sections with headers and detailed paragraphs. 
            Elaborate each section with detailed explanations and examples. 
            Use research, data, and references to expand the content and make it very informative.

            ### STRUCTURE:
            1. Introduction - Set the context and explain why the topic is important.
            2. Body - Break down the blog into 3-4 major sections, each with its own header and multiple paragraphs.
            3. Conclusion - Summarize key points and include a final thought or call to action.

            ### FORMATTING:
            - Use <h2> tags for section headers and <p> tags for paragraphs and <h1> for title.
            - Ensure the blog has more than {word_limit} words.
            - Include 3 to 4 references at the end of the blog.
            
            ### REFERENCES:
            At the end of the blog, include 3 to 4 credible references for the topic.
            ###BLOG MUST CONTAIN MORE THAN {word_limit} WORDS:
            ### BLOG MUST EXCEED {word_limit} WORDS:
            (NO PREAMBLE)
            """
        )
        
        chain = prompt | llm
        res = chain.invoke({
            "blog_topic": blog_topic,
            "word_limit": word_limit,
            "blog_style": blog_style,
            "tone": tone
        })
        logging.info("Blog generated successfully.")
        return res.content
    except Exception as e:
        logging.error("Failed to generate blog: %s", e)
        raise

def generate_title(llm, blog_topic):
    if not blog_topic:
        raise ValueError("Please provide a valid blog topic.")
    try:
        prompt = PromptTemplate.from_template(
            """
            ### BLOG TOPIC:
            {blog_topic}
            
            ### INSTRUCTIONS:
            Generate a catchy and SEO-friendly blog title for the topic above.
            Ensure it grabs the reader's attention.

            ### ONLY TITLE (NO PREAMBLE):
            """
        )
        
        chain = prompt | llm
        res = chain.invoke({"blog_topic": blog_topic})
        logging.info("Title generated successfully.")
        return res.content.strip()
    except Exception as e:
        logging.error("Failed to generate title: %s", e)
        raise

def suggest_blog_topics(llm):
    try:
        prompt = PromptTemplate.from_template(
            """
            ### INSTRUCTIONS:
            Generate 5 unique and creative blog topic ideas that span a diverse range of subjects. These topics should encompass areas such as technology, science, lifestyle, health, travel, personal development, and any emerging trends or phenomena that may captivate a wide audience. 

            For each topic, consider the following:
            - **Relevance**: Ensure the topics align with current trends and resonate with contemporary issues or interests.
            - **Interest Factor**: Aim for topics that are intriguing and provoke thought, encouraging readers to explore further.
            - **Diversity of Audience**: Select themes that appeal to various demographics, including different age groups, backgrounds, and interests.
            - **Depth and Scope**: Choose topics that allow for in-depth exploration, offering opportunities for research, discussion, and detailed analysis.

            ### EXAMPLES OF POSSIBLE TOPIC CATEGORIES:
            1. **Technology**: Innovations, ethical implications, future predictions.
            2. **Science**: Recent discoveries, environmental issues, space exploration.
            3. **Lifestyle**: Trends in wellness, sustainable living, digital nomadism.
            4. **Health**: Mental health, nutrition, fitness trends.
            5. **Travel**: Off-the-beaten-path destinations, travel tips, cultural insights.
            6. **Personal Development**: Mindfulness practices, productivity hacks, lifelong learning.

            ### TOPIC IDEAS (ONLY TITLES, NO PREAMBLE):
            """

        )
        
        chain = prompt | llm
        res = chain.invoke({})
        logging.info("Blog topics generated successfully.")
        return res.content.strip().split('\n')
    except Exception as e:
        logging.error("Failed to generate blog topics: %s", e)
        raise

def generate_blog_tags(llm, blog_content):
    if not blog_content:
        raise ValueError("Blog content cannot be empty for generating tags.")
    try:
        prompt = PromptTemplate.from_template(
                    """
            ### BLOG CONTENT:
            {blog_content}

            ### INSTRUCTIONS:
            Based on the blog content provided, generate 5 unique and SEO-friendly tags that effectively capture the essence of the article. These tags should:
            - **Be Relevant**: Ensure each tag directly relates to the main topics and themes discussed in the blog content.
            - **Utilize Keywords**: Incorporate keywords or phrases that potential readers might use in search queries, optimizing for search engine visibility.
            - **Encourage Engagement**: Aim for tags that are compelling and engaging, encouraging readers to click and explore further.
            - **Be Concise**: Each tag should be brief yet descriptive, ideally no more than 3-5 words.
            - **Consider Variations**: Include a mix of broad and specific tags to attract a wider audience while also targeting niche readers.

            ### TAGS:
            """
        )
        
        chain = prompt | llm
        res = chain.invoke({"blog_content": blog_content})
        logging.info("Tags generated successfully.")
        return res.content.strip().split(',')
    except Exception as e:
        logging.error("Failed to generate tags: %s", e)
        raise

def generate_blog_outline(llm, blog_topic):
    if not blog_topic:
        raise ValueError("Blog topic cannot be empty for generating an outline.")
    try:
        prompt = PromptTemplate.from_template(
            """
            ### BLOG TOPIC:
            {blog_topic}

            ### INSTRUCTIONS:
            Develop a comprehensive outline for a blog post based on the given topic. The outline should include the following components:

            1. **Title**: Craft a compelling title that captures the essence of the blog and attracts readers.
            2. **Introduction**: Briefly outline what the blog will cover, setting the context and explaining its relevance to the audience. Include a hook to engage readers.
            3. **Main Sections**: Identify 3-5 key sections or subtopics that will be explored in the blog. For each section, provide:
            - **Header**: A descriptive header that summarizes the content of the section.
            - **Bullet Points**: Key points, ideas, or arguments that will be discussed in that section.
            - **Examples or Data**: Suggestions for examples, data, or anecdotes that can be included to support the section.

            4. **Conclusion**: Summarize the main points of the blog and provide a final thought or call to action, encouraging readers to engage further with the topic.
            5. **References**: Suggest potential sources or references that could be cited in the blog for credibility and additional reading.

            ### OUTLINE:
            """

        )
        
        chain = prompt | llm
        res = chain.invoke({"blog_topic": blog_topic})
        logging.info("Outline generated successfully.")
        return res.content.strip()
    
    except Exception as e:
        logging.error("Failed to generate blog outline: %s", e)
        raise
