import matplotlib.pyplot as plt

gene_list     =   ["gene_name \ninformation","gene2 \ninformation2","gene 3\ninformation3"]
distance_list =   ["+23 bp", "+45 bp"]

def gene_figure(xsize, ysize, gene_list, distance_list, title, font):
    plt.figure(figsize=(xsize,ysize))
    ax=plt.subplot(111)
   
    zipped_list = zip(gene_list, distance_list)
    
    annotation1 = ax.annotate(gene_list.pop(0), xy=(0, 0.5), xycoords="data",
                      va="center", ha="center", size=15,
                      bbox=dict(boxstyle="rarrow", fc="w"))
    annotation2 = annotation1 
    
    
    for item in zipped_list:
        (gene,distance) = item
    
        annotation2 = ax.annotate(gene, xy=(1.0, 0.5), xycoords=annotation1.get_window_extent,
                          xytext=(30,0), textcoords="offset points",
                          va="center", ha="left", size=15,
                          bbox=dict(boxstyle="rarrow", fc="w"))
        arrow = ax.annotate(distance,
                    xy=(0.5, 1.5), xycoords=annotation2.get_window_extent,
                    xytext=(1, 1.5), textcoords=annotation1.get_window_extent,
                    arrowprops=dict(arrowstyle="->",
                                    connectionstyle="arc3,rad=-0.3"),
                    )
        annotation1 = annotation2
    
    
    plt.axis('off')
    plt.tight_layout()
    plt.title(title,fontsize=font)
    plt.show()


gene_figure(1,2,gene_list,distance_list, "Title", 40)



