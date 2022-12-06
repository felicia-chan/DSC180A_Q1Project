import pandas as pd
import os

def get_content_and_cites(citeseer_cites, citeseer_content):
    '''
    Returns two DataFrames: one of the processed citeseer_cites, 
    and one of processed citeseer_content. Use indexing to access individual dataframes.
    '''
    citeseer_cites = pd.read_csv(citeseer_cites, 
                             sep='\t', 
                             header=None, 
                             names=['target', 'source'])
    
    citeseer_cites['target'] = citeseer_cites['target'].astype(str)
    citeseer_cites['source'] = citeseer_cites['source'].astype(str)
    
    citeseer_features = [f"f{i}" for i in range(3703)]
    citeseer_content = pd.read_csv(citeseer_content,
                                   sep="\t",
                                   header=None,
                                   names=["id", *citeseer_features, "class"]
    )
    
    # make sure that id are all string since some are int
    citeseer_content['id'] = citeseer_content['id'].astype(str)
    # turn id into index
    citeseer_content_str_subject = citeseer_content.set_index("id")
    
    # create lists of unused nodes
    source_remove = ['ghani01hypertext', 'nielsen00designing', 'kohrs99using', 'wang01process', 'hahn98ontology', '293457', 'gabbard97taxonomy']
    target_remove = ['197556', '38137', '95786', 'flach99database', 'khardon99relational', 'kohrs99using', 'raisamo99evaluating', 'tobies99pspace', 'weng95shoslifn']
    # remove unnecessary nodes from source + target
    citeseer_cites_copy = citeseer_cites[~citeseer_cites.source.isin(source_remove)]
    citeseer_cites_copy = citeseer_cites_copy[~citeseer_cites_copy.target.isin(target_remove)]
    citeseer_cites_copy = citeseer_cites_copy.reset_index(drop=True)
    citeseer_content_feats = citeseer_content_str_subject.loc[:, 'f0':'f3702'] # features only
    
    return citeseer_content_feats, citeseer_cites_copy

def get_data(citeseer_content_feats, citeseer_cites, outpath):
    '''
    Uses dataframes and saves them as csv files in the output directory.
    
    :param: citeseer_content_feats: dataframe of node features
    :param: citeseer_cites: dataframe of edge features
    :param: outpath: directory to save the data in.
    '''
    citeseer_content_feats.to_csv(os.path.join(outpath, "citeseer_content_feats"+".csv"))
    citeseer_cites.to_csv(os.path.join(outpath, "citeseer_cites"+".csv"))
    return