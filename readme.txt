July 21, 2015
Matt Payne
www.pattmayne.com


BLOG APP:

The BLOG app contains all the html files because a BLOG is a public fixture.

The BLOG app contains the MODELS which define things related to the blog, such as articles.

It also contains (currently) the views.py files which control the backend, for creating both articles and database entries.



INDIE_DB APP:

The INDIE_DB app contains (currently) the views.py file which controls the front end.

It also contains the MODELS which define database entries such as Artist, Work (of art), Production Company, etc.



I SHOULD PROBABLY SWITCH THE VIEWS between Blog and Indie_DB, since BLOG deals more with frontend stuff and INDIE_DB deals more with database/backend stuff. But IF I DON'T do this, anybody reading this will have a heads up about this counterintuitive  setup.