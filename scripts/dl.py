import streamlit as st
import sys
import os
from openai import OpenAI
import datetime
import time

# Import the search_and_extract function from google-latest.py
from data.google_scrape import search_and_extract

# Initialize OpenAI client
client = OpenAI()

def distill_individual_article(article, user_query):
    """
    Process individual article with GPT-4-turbo to extract all relevant information
    """
    # Create prompt for reasoning model
    prompt = f"""
    Analyze the following news article content and extract ALL relevant information, facts, and insights,
    even if they seem only tangentially related to the query: "{user_query}"
    
    SOURCE URL: {article['url']}
    PUBLICATION DATE: {article['publication_date']}
    
    CONTENT:
    {article['content']}
    
    Distill this article into key facts, quotes, statistics, and insights. Be comprehensive and capture ALL useful information,
    not just what seems immediately relevant to the query. Format your response as a bulleted list of clear, concise points.
    """
    
    try:
        # Using GPT-4-turbo as the reasoning model to distill information from each article
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Using GPT-4-turbo for distillation
            messages=[
                {"role": "system", "content": "You are an expert analyst who extracts and distills all key information from content. Be thorough and comprehensive."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        return {
            "url": article['url'],
            "publication_date": article['publication_date'],
            "distilled_content": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "url": article['url'],
            "publication_date": article['publication_date'],
            "distilled_content": f"Error in distillation: {str(e)}"
        }

def generate_report_from_distilled_content(distilled_articles, user_query):
    """
    Generate a comprehensive report from all distilled article content
    """
    # Prepare distilled content for the report generation model
    combined_distilled_content = "\n\n".join([
        f"Source: {item['url']}\nDate: {item['publication_date']}\n{item['distilled_content']}" 
        for item in distilled_articles
    ])
    
    # Create prompt for report generation
    prompt = f"""
    Based on the following distilled information from multiple articles, create a comprehensive analysis report
    addressing this query: {user_query}
    
    DISTILLED CONTENT FROM ARTICLES:
    {combined_distilled_content}
    
    Please structure your report with clear sections, bullet points where appropriate, 
    and highlight key insights. Format your response in markdown.
    """
    
    try:
        # Using GPT-4-turbo for generating the final report
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Using GPT-4-turbo for the final report generation
            messages=[
                {"role": "system", "content": "You are an expert analyst who creates detailed, well-structured reports based on distilled information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in report generation: {str(e)}"

def main():
    st.title("News Search and Analysis Application")
    
    # Get user inputs
    user_query = st.text_input("Enter your search query:")
    want_recent = st.checkbox("Do you want only recent news?")
    
    # Create a search button
    search_button = st.button("Search")
    
    # Initialize session state for distillation if it doesn't exist
    if 'distillation_in_progress' not in st.session_state:
        st.session_state.distillation_in_progress = False
    
    # When search button is clicked and query is not empty
    if search_button and user_query:
        with st.spinner("Searching for news..."):
            try:
                # Call the search_and_extract function with user inputs
                results = search_and_extract(user_query, want_recent)
                
                # Store results in session state for later use
                st.session_state.search_results = results
                
                # Filter out forbidden URLs for display count
                accessible_results = [r for r in results if not r['content'].startswith("Error: HTTP error 403 Client Error: Forbidden for url:")]
                
                # Display the results
                if results:
                    st.success(f"Found {len(results)} results total, {len(accessible_results)} accessible")
                else:
                    st.warning("No results found for your query.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    elif search_button and not user_query:
        st.warning("Please enter a search query.")
    
    # Check if there are already results in the session state (for when users switch tabs)
    if hasattr(st.session_state, 'search_results') and st.session_state.search_results:
        results = st.session_state.search_results
        
        # Filter out forbidden URLs for display count
        accessible_results = [r for r in results if not r['content'].startswith("Error: HTTP error 403 Client Error: Forbidden for url:")]
        
        st.success(f"Found {len(results)} results total, {len(accessible_results)} accessible")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["URLs Only", "Detailed View", "Distilled Content", "Generate Report"])
        
        with tab1:
            # Display just the URLs
            st.subheader("URLs")
            for i, item in enumerate(results, 1):
                # Add indicator for forbidden URLs
                if item['content'].startswith("Error: HTTP error 403 Client Error: Forbidden for url:"):
                    st.write(f"{i}. {item['url']} ⚠️ (Access Forbidden)")
                else:
                    st.write(f"{i}. {item['url']}")
        
        with tab2:
            # Display detailed information
            st.subheader("Detailed Results")
            for i, item in enumerate(results, 1):
                # Add indicator for forbidden URLs in the expander title
                title = f"Result {i}: {item['url']}"
                if item['content'].startswith("Error: HTTP error 403 Client Error: Forbidden for url:"):
                    title += " ⚠️ (Access Forbidden)"
                
                with st.expander(title):
                    st.write(f"**URL:** {item['url']}")
                    st.write(f"**Publication Date:** {item['publication_date']}")
                    st.text_area(f"Content {i}", item['content'], height=200)
        
        with tab3:
            st.subheader("Distilled Article Content")
            st.write("Process each article individually to extract key information.")
            
            # Container for distillation status updates
            distillation_status = st.empty()
            
            # Container for detailed progress messages
            detailed_progress = st.container()
            
            # Only show distill button if not currently distilling
            if not st.session_state.distillation_in_progress:
                if st.button("Distill Articles"):
                    # Set the flag to indicate distillation is in progress
                    st.session_state.distillation_in_progress = True
                    
                    # Rerun to refresh the UI immediately
                    st.rerun()
            
            # If distillation is in progress, show the progress and perform the distillation
            if st.session_state.distillation_in_progress:
                # Filter out content with 403 errors
                filtered_content = [item for item in results if not item['content'].startswith("Error: HTTP error 403 Client Error: Forbidden for url:")]
                
                # Show initial status message
                distillation_status.info(f"Starting distillation process for {len(filtered_content)} articles...")
                
                # Initialize distilled articles in session state
                st.session_state.distilled_articles = []
                
                # Process each article individually
                progress_bar = st.progress(0)
                
                # Create placeholders for updates
                article_progress = st.empty()
                article_details = st.empty()
                processing_status = st.empty()
                completion_status = st.empty()
                
                for i, article in enumerate(filtered_content):
                    # Update the status message with current article
                    current_article_title = article['url'].split('/')[-1] if '/' in article['url'] else article['url']
                    article_progress.info(f"Distilling article {i+1}/{len(filtered_content)}: Processing '{current_article_title}'")
                    
                    # Display article details
                    article_details.markdown(f"""
                    🔍 **Analyzing**: {article['url']}  
                    📅 **Published**: {article['publication_date']}  
                    """)
                    
                    # Show processing status
                    processing_status.warning("⏳ Extracting key information...")
                    
                    # Distill the article
                    distilled = distill_individual_article(article, user_query)
                    st.session_state.distilled_articles.append(distilled)
                    
                    # Update progress bar
                    progress_bar.progress((i + 1) / len(filtered_content))
                    
                    # Indicate completion of this article
                    completion_status.success(f"✅ Completed distillation of article {i+1}: {article['url']}")
                    
                    # Add a visual separator
                    st.write("---")
                    
                    # Ensure UI updates by forcing a small delay
                    time.sleep(0.1)
                
                # Show completion message
                distillation_status.success(f"Successfully distilled {len(st.session_state.distilled_articles)} articles.")
                
                # Reset the flag since distillation is complete
                st.session_state.distillation_in_progress = False
                
                # Force a rerun to refresh the UI
                st.rerun()
            
            # Display distilled content if available
            if hasattr(st.session_state, 'distilled_articles') and st.session_state.distilled_articles:
                st.subheader("Distilled Content")
                for i, item in enumerate(st.session_state.distilled_articles, 1):
                    with st.expander(f"Distilled Content {i}: {item['url']}"):
                        st.write(f"**URL:** {item['url']}")
                        st.write(f"**Publication Date:** {item['publication_date']}")
                        st.markdown(item['distilled_content'])
        
        with tab4:
            st.subheader("Generate Analysis Report")
            st.write("Generate a detailed analysis report based on distilled article content.")
            
            # Check if we have distilled articles
            if hasattr(st.session_state, 'distilled_articles') and st.session_state.distilled_articles:
                analysis_query = st.text_area("Specify what you want to analyze about these results:", 
                                             value=user_query, height=100)
                
                report_status = st.empty()
                
                if st.button("Generate Report"):
                    with st.spinner("Generating comprehensive report from distilled content..."):
                        report_status.info("Creating comprehensive analysis report... This may take a moment.")
                        
                        # Generate report using distilled content
                        report_content = generate_report_from_distilled_content(
                            st.session_state.distilled_articles, 
                            analysis_query
                        )
                        
                        # Display the report in Streamlit
                        report_status.success("Report generated successfully!")
                        st.subheader("Generated Report")
                        st.markdown(report_content)
            else:
                st.warning("Please distill the articles first in the 'Distilled Content' tab.")

if __name__ == "__main__":
    main()