from pathlib import Path
import pylexibank
from clldutils.misc import slug

SUPPLEMENT = "http://www.pnas.org/content/suppl/2016/11/10/1613666113.DCSupplemental/pnas.1613666113.st01.docx"

class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "hayniecolorterms"

    # define the way in which forms should be handled
    form_spec = pylexibank.FormSpec(
        brackets={"(": ")", "[": "]"},  # characters that function as brackets
        separators=";/,",  # characters that split forms e.g. "a, b".
        missing_data=('?', '-'),  # characters that denote missing data.
        strip_inside_brackets=True   # do you want data removed in brackets or not?
    )

    def cmd_download(self, args):
        # Note this downloads the raw data:
        # self.raw_dir.download(SUPPLEMENT, "pnas.1613666113.st01.docx")
        # ... but we're using a hand-edited version, so make this a no-op.
        pass
    
    def cmd_makecldf(self, args):
        args.writer.add_sources()
        languages = args.writer.add_languages(lookup_factory="Name")
        
        # concepts = args.writer.add_concepts(
        #     id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
        #     lookup_factory="Name"
        # )
        concepts = {}
        for i, concept in enumerate(self.concepts, 1):
            cid = "%d_%s" % (i, slug(concept['Gloss']))
            args.writer.add_concept(
                ID=cid,
                Name=concept['Gloss'],
                Concepticon_ID=concept['Concepticon_ID'],
                Concepticon_Gloss=concept['Concepticon_Gloss']
            )
            concepts[concept['Gloss']] = cid
        
        for row in self.raw_dir.read_csv("pnas.1613666113.st01.txt", dicts=True, delimiter="\t"):
            lang = row.pop("")
            for col in row:
                lex = args.writer.add_forms_from_value(
                    Language_ID=languages[lang],
                    Parameter_ID=concepts[col],
                    Value=row[col],
                    Source=['Haynie2016'],
                )
