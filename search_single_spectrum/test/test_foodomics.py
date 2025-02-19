import pandas as pd
import unittest
import sys
import os
sys.path.insert(0, "../tools/search_single_spectrum/")
sys.path.insert(0, "tools/search_single_spectrum/")
import foodomics_track

sys.path.insert(0, "../tools/search_single_spectrum/interactive_tree_js/")
sys.path.insert(0, "tools/search_single_spectrum/interactive_tree_js/")
import build_tree


class TestLoaders(unittest.TestCase):
    def test(self):
        input_filename = "data/foodomics/all_dataset_matchs.tsv"
        foodomics_metadata = "../tools/search_single_spectrum/gfop_ontology_foodmasst.txt"
        foodomics_metadata_table = "../tools/search_single_spectrum/foodomics_metadata_foodmasst.tsv"

        out_foodmasst = "tmp/out_foodmasst.tsv"
        out_filtered_food_metadata = "tmp/out_filtered_food_metadata.tsv"

        # run
        foodomics_track.combine_food_masst(foodomics_metadata, foodomics_metadata_table, input_filename, out_foodmasst, \
        out_filtered_food_metadata)

        # ground truth test file
        test_output = pd.read_csv("data/foodomics/foodmasst_test_output.tsv", sep="\t")
        test_matches_filtered = pd.read_csv("data/foodomics/filtered_food_metadata.tsv", sep="\t")

        # read back results from tmp files
        enrichment_df = pd.read_csv(out_foodmasst, sep="\t")
        matches_filtered = pd.read_csv(out_filtered_food_metadata, sep="\t")

        # actual test - ignore sorting
        pd.testing.assert_frame_equal(test_matches_filtered, matches_filtered, check_like=True)
        pd.testing.assert_frame_equal(test_output, enrichment_df, check_like=True)


    def test_empty_matches(self):
        input_filename = "data/foodomics/all_dataset_matchs_empty.tsv"
        foodomics_metadata = "../tools/search_single_spectrum/gfop_ontology_foodmasst.txt"
        foodomics_metadata_table = "../tools/search_single_spectrum/foodomics_metadata_foodmasst.tsv"

        out_foodmasst = "tmp/out_foodmasst_empty.tsv"
        out_filtered_food_metadata = "tmp/out_filtered_food_metadata_empty.tsv"

        # run
        foodomics_track.combine_food_masst(foodomics_metadata, foodomics_metadata_table, input_filename, out_foodmasst, \
        out_filtered_food_metadata)

        # should be empty file
        self.assertTrue(os.path.isfile(out_foodmasst), "No enrichment file exported")
        self.assertFalse(os.path.getsize(out_foodmasst) > 0, "Enrichment file is not empty - was expected for an empty "
                                                             "input")

        self.assertTrue(os.path.isfile(out_filtered_food_metadata), "No metadata table file exported")
        self.assertFalse(os.path.getsize(out_filtered_food_metadata) > 0, "Metadata table file is not empty - was "
                                                                          "expected for an empty input")

    def test_food_tree(self):
        test_output = "data/foodomics/foodmasst_test_output.tsv"
        in_html = "../tools/search_single_spectrum/interactive_tree_js/collapsible_tree_v3.html"
        in_ontology = "../tools/search_single_spectrum/interactive_tree_js/GFOP.json"

        out_json = "tmp/tree.json"
        out_html = "tmp/tree.html"
        build_tree.create_tree_html(in_html, in_ontology, test_output,out_json,True,out_html,True)

        # not empty
        if os.path.getsize(out_json) <= 0:
            raise RuntimeError("Tree data json file is empty")
        if os.path.getsize(out_html) <= 0:
            raise RuntimeError("Tree data json file is empty")



if __name__ == '__main__':
    unittest.main()