import pandas as pd
#!pip install wordcloud -q
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# import csv
data = pd.read_csv('data-tweets-nlp.csv')

#------------------------------------------------------------------------------------
'''
Select 5 lists of words in .txt format

       Parameters
       ----------
    List_Human = words clasified as human sounds
    List_Techno = words clasified as tecnological sounds
    List_Nature = words clasified as nature sounds
    List_all_descriptors = all descriptors translated based on ISO 1913 descriptor 
                            terms in english. This words will be the characters to search.
    List_selected_descriptors = selected descriptors based on temporal analyses
'''

def open_lst(lst): 
    with open("%s.txt" %lst, encoding="utf8") as f:
        x = f.readlines()
    x = " ".join(s for s in x ).split(',')
    x = [i.strip(" ").strip("\n").strip(" ") for i in x]
    return x

Selected_descriptors = open_lst("Selected_descriptors")
All_descriptors = open_lst("All_descriptors")
Human = open_lst("Human")
Techno = open_lst("Techno")
Nature = open_lst("Nature")


#------------------------------------------------------------------------------------
'''Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
 '''

class SimpleGroupedColorFunc(object):
    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)
    
#------------------------------------------------------------------------------------
'''
Iterate throught desciptors in list in ordr to create the wordcloud
The words present in wordcloud must be in the 3 lists  previously created.

       Parameters
       ----------
       Paste named wordcloud must exist in the same paste

'''
# descriptor = "tranquilo"
for descriptor in Selected_descriptors:  
    df_mask=data['type_list2']=="%s" %descriptor
    data_type = data[df_mask]   
    data_type = data_type.reset_index()
    del data_type["index"]
    #----------------data_type = data
    
    list_Nature = []
    list_Techno = []
    list_Human = []
    list_total = []
    
    #------------------------------------------------------------------------------------
    # Create lists based on words in tweets
    for row in data_type.index:
        word_list = data_type['words'][row].split(', ')
        
        for i in range(len(word_list)):
            for k in range(len(Nature)):
                if word_list[i] == Nature[k]:
                    list_Nature.append(word_list[i])
                    list_total.append(word_list[i])
            for k in range(len(Techno)):
                if word_list[i] == Techno[k]:
                    list_Techno.append(word_list[i])
                    list_total.append(word_list[i])
            for k in range(len(Human)):
                if word_list[i] == Human[k]:
                    list_Human.append(word_list[i])
                    list_total.append(word_list[i])
            
    all_words = " ".join(s for s in list_total)
    text = all_words
    
    # Since the text is small collocations are turned off and text is lower-cased
    wc = WordCloud(collocations=False,background_color="white").generate(text.lower())
    
    # words below will be colored with a green single color function
    color_to_words = {"#ffc222": Human, #YELOW
        "#FF0000": Techno, #RED
        "#5391c7": Nature} #BLUE 
    
    # Words that are not in any of the color_to_words values
    # will be colored with a grey single color function
    default_color = "grey"
    
    # Create a color function with single tone
    grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)
    
    # Apply our color function
    wc.recolor(color_func=grouped_color_func)
    
    # Show and save the wordcloud
    fig, ax = plt.subplots(figsize=(16,8))            
    ax.imshow(wc, interpolation='bilinear')       
    ax.set_axis_off()
    plt.imshow(wc)             
    wc.to_file("/wordcloud/colored-%s.jpg"  %descriptor,);
    




