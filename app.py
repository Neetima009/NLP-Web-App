#Core packages
import streamlit as st
st.set_page_config(page_title="NLP Simple Examples", page_icon="web_logo.jpg", layout='centered', initial_sidebar_state='auto')


#NLP packages
from textblob import TextBlob
import neattext as nt
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
from googletrans import Translator
from wordcloud import WordCloud

#Viz Packages
import  matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')



#Function for Text Summary
def  summarize(txt, ratio=0.2):

    nlp = spacy.load("en_core_web_sm")
    
    doc = nlp(txt)

    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']

    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)

    freq_word = Counter(keyword)
    freq_word.most_common(5)

    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word]/max_freq)
    freq_word.most_common(5)

    sent_strength={}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent]+=freq_word[word.text]
                else:
                    sent_strength[sent]=freq_word[word.text]
    
                
    summarized_sentences = nlargest(3, sent_strength, key=sent_strength.get)
    

    final_sentence = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentence)
    return summary

#Function For Tokens and Lemma Analysis
@st.cache_data
def text_analyzer(my_text):
    nlp = spacy.load("en_core_web_sm")
    docx = nlp(my_text)
    allData = [('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_))for token in docx]
    return allData

#Function For Wordcloud Plotting
def plot_wordcloud(my_text):
    mywordcloud = WordCloud().generate(my_text)
    fig = plt.figure(figsize=(20,10))
    plt.imshow(mywordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)



def main():
    """NlP App with Streamlit and TextBlob"""
    
    title_templ = """
    <div style="background-color:orange;padding:10px;">
    <h2 style="color:blue">NLP Simple Examples</h2>
    </div>
    """
    st.markdown(title_templ, unsafe_allow_html=True)


    subheader_templ = """
    <div style="background-color:cyan;padding:8px;">
    <h4 style="color:bue">Natural Language Processing On the GO...</h4>
    </div>
    """
    st.markdown(subheader_templ, unsafe_allow_html=True)    

    st.sidebar.image("web_logo.jpg", use_column_width=True)
    

    # Menu Sidebar
    activity = ["Text Analysis", "Translation",  "Sentiment Analysis","About"]
    choice = st.sidebar.selectbox("Menu",activity)
    
    # Text Analysis CHOICE
    if choice == "Text Analysis":

        st.subheader("Text Analysis")
        st.write("")
        st.write("")
        raw_text = st.text_area("Write something","Enter your text in English...", height=250)

        if st.button("Analyse"):

            if len(raw_text) == 0:
                st.warning("Enter a Text...")
            else:
                blob = TextBlob(raw_text)
                #st.write("good")

                #if raw_text != '':
                #    st.warning("Enter the Text ...")
                #else:
                st.info("Basic Functions")
                col1, col2 = st.columns(2)

                with col1:
                    with st.expander("Basic Info"):
                        st.write("Text Stats") #st.success
                        word_desc = nt.TextFrame(raw_text).word_stats()
                        result_desc = {"Length of Text":word_desc['Length of Text'],
                                        "Number of Vowels":word_desc['Num of Vowels'],
                                        "Num of Consonents":word_desc['Num of Consonants'],
                                        "Num of Stopwords":word_desc['Num of Stopwords']}
                        st.write(result_desc)
                    
                    with st.expander("Stopwords"):
                        st.success("Stop Words List")
                        stop_w = nt.TextExtractor(raw_text).extract_stopwords()
                        st.error(stop_w)

                with col2:
                    with st.expander("Processed Text"):
                        st.success("Stopwords Excluded Text")
                        processed_text = str(nt.TextFrame(raw_text).remove_stopwords())
                        st.write(processed_text)

                    with st.expander("Plot Wordcloud"):
                        st.success("Wordcloud")
                        plot_wordcloud(raw_text)

                        
                st.write("")
                st.write("")
                st.info("Advanced Features")
                col3, col4 = st.columns(2)

                with col3:
                    with st.expander("Tokens and lemma"):
                        processed_text_mid = str(nt.TextFrame(raw_text).remove_stopwords())
                        processed_text_mid = str(nt.TextFrame(processed_text_mid).remove_puncts())
                        processed_text_fin = str(nt.TextFrame(processed_text_mid).remove_special_characters())
                        tandl = text_analyzer(processed_text_fin)
                        st.json(tandl)
                        #st.write("T&L")

                with col4:
                    with st.expander("Summarize"):
                        st.success("Summarize")
                        summary_text = summarize(raw_text, ratio=0.4) 
                        if summary_text != "":
                            st.success(summary_text)
                        else:
                            st.warning("Please insert a Longer Text")




    elif choice == "Translation":

        st.subheader("Text Translation")
        st.write("")
        st.write("")
        raw_text = st.text_area("Insert Your Text","Write something to be translated...")
        if len(raw_text) < 3:
            st.warning("Please  Insert More Than Three Characters!")
        else:
            translator = Translator()
            lang = translator.detect(raw_text)
            st.write(lang.lang)
            tran_option = st.selectbox("Select translation language",["English","Spanish","Chinese","French","German","Italian","Hindi"])
            if st.button("Translate"):
                if tran_option =='Italian' and lang != 'it':
                    st.text("Translating to Italian...")
                    tran_result = translator.translate(raw_text, dest='it')
                elif tran_option =='Spanish' and lang != 'es':
                    st.text("Translating to Spanish...")
                    tran_result = translator.translate(raw_text, dest='es')
                elif tran_option =='Chinese' and lang != 'zh-CN':
                    st.text("Translating to Chinese...")
                    tran_result = translator.translate(raw_text, dest='zh-CN')
                elif tran_option =='French' and lang != 'Fr':
                    st.text("Translating to French...")
                    tran_result = translator.translate(raw_text, dest='Fr')
                elif tran_option =='Russian' and lang != 'ru':
                    st.text("Translating to Russian...")
                    tran_result = translator.translate(raw_text, dest='ru')
                elif tran_option =='German' and lang != 'de':
                    st.text("Translating to German...")
                    tran_result = translator.translate(raw_text, dest='de')
                elif tran_option =='English' and lang != 'en':
                    st.text("Translating to English...")
                    tran_result = translator.translate(raw_text, dest='en')
                elif tran_option =='Hindi' and lang != 'hi':
                    st.text("Translating to Hindi...")
                    tran_result = translator.translate(raw_text, dest='hi')
                else:
                    tran_result = "Text is already in " + "'" + lang+ "'"
                    
                st.success(tran_result.text)


    if choice == "Sentiment Analysis":

        st.subheader("Sentiment Analysis")
        st.write("")
        st.write("")

        raw_text = st.text_area("", "Enter Text Here...")
        if st.button("Evaluate"):
            
            if len(raw_text)==0:
                st.warning("Enter a Text...")
            else:
                translator = Translator()
                lang = translator.detect(raw_text)
                lang = lang.lang

                if lang != 'en':
                    tran_result = translator.translate(raw_text, dest='en')
                    blob = TextBlob(str(tran_result))
                
                else:
                    blob = TextBlob(raw_text)

                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
                st.info("Sentiment Polarity: {}".format(polarity))
                st.info("Sentiment Subjectivity: {}".format(subjectivity))

    
    if choice == "About":

        st.subheader("About")
        st.write("")
        st.write("")

        st.markdown("""
        ### NLP Simple Examples (App with Streamlit and Spacy)                    
        + **Author:** [Neetima Verma](https://www.linkedin.com/in/neetima-verma-data-scientist/)
                    
        """)





if __name__ == '__main__':
    main()


