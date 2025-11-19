Slime Mold Graph Repository
Version 1.0
Mehlhorn, Tim; Dirnberger, Michael, 2025, "Slime Mold Graph Repository", https://doi.org/10.17617/3.XWST2Q, Edmond, V1
Cite Dataset
Download EndNote XML
Download RIS
Download BibTeX
View Styled Citation
Learn about Data Citation Standards.
Access Dataset
The dataset is too large to download. Please select the files you need from the files table.
Contact Owner
Share
Dataset Metrics
100 Downloads
Description
The KIST Europe Data Set
Introduction
This dataset focuses on networks formed by Physarum Polycephalum. Detailed methods are available in the companion paper.
Description
The KIST Europe data set contains raw and processed data of 81 identical experiments, carefully executed under constant laboratory conditions. The data was produced using the following procedure:
A rectangular plastic dish is prepared with a thin sheet of agar.
A small amount of dried P. Polycephalum (HU195xHU200) sclerotia crumbs is lined up along the short edge of the dish. The dish is put into a large light-proof box.
After approximately 14 hours the plasmodium has resuscitated and starts exploring the available space towards the far side of the dish. Typically, the apical zone needs to cover a distance of several centimeters before network formation can be observed properly.
For the next 30 hours we take a top-view image of the growing plasmodium and its changing network every 120 seconds from a fixed position. We stop capturing when the apical zone is about to reach the far side of the dish, which is outside of the observed area.
After obtaining sequences of images showing the characteristic networks of P. Polycephalum, we use a software called NEFI to compute corresponding sequences of graph representations of the depicted structures within a predefined region of interest. In addition to the topology the graphs store precise information of the length and width of the edges as well as the coordinates of the nodes in the plane.
Given the resulting sequence of graphs we apply filters removing artifacts and other unwanted features of the graphs. Then we proceed to compute a novel node tracking, encoding the time development of every node, taking into account the changing topology of the evolving graphs.
Repeating this experiment we obtain 81 sequence of images, which we consider our raw data. We stress at this point that given the inherently uncontrollable growth process of P. Polycephalum, the obtained sequences differ in length and nature. That is to say, in some experiments the organism behaved unfavorably, simply stopping its growth, changing direction or even escaping the container. While such sequences are part of the raw dataset, we excluded them partially or completely from the subsequent graph extraction efforts. The removal of such data reduces the number of series depicting proper network formation to 54.
After obtaining the raw data, we transform the images into equivalent mathematical graphs, thus opening up a wealth of possibilities for data analysis. To this end we deploy a convenient automatic software tool called NEFI, which analyzes a digital image, separates the depicted slime mold network from the background and returns a graph representation of said structure. Using this tool effectively requires some moderate amount of image preprocessing. In particular, for each sequence of images it is necessary to decide on a suitable subsequence to be processed. Here we typically exclude parts of the sequence where the apical zone is still visible. For each such subsequence a suitable region of interest is defined manually. The graph stores the position of the nodes in the plane as well as edge attributes such as edge length and widths for each edge. In addition to the output of NEFI including the unfiltered graphs, the dataset contains NEFI's input, i.e. the selected subsequences of images cropped according to their defined regions of interest.
Note that some parts of the image series showing proper network formation did not yield optimal representations of the depicted networks. This is a result of images exhibiting strong color gradients rendering them too challenging for automatic network extraction. While such cases can still be handled by tuning the parameters of image processing manually on an image per image basis, we decided to discard affected series from subsequent processing efforts. As a result the number of usable graph sequences of highest quality reduced to 36 to which we apply a set of filters removing artifacts, isolated small components and dead-end paths. Thus we obtain a total of 3134 distinct filtered graphs faithfully reflecting the topology and edge attributes that P. Polycephalum displayed during the wet-lab experiments. At this point available graph analysis packages or custom written analysis code can be deployed to investigate the data in various ways. The dataset includes the filtered graphs as well as all corresponding graph drawings. The latter enable a quick visual inspection of the results of the graph extraction.
Given the obtained time-ordered sequences of graphs the development of the entire graph can be investigated. However, one may also study what happens to single nodes as P. Polycephalum evolves. Given a graph in a time ordered sequence of graphs, let us pick any node u. Can we find pick a set of nodes from graphs in the sequence that are equivalent to u, that is, all nodes in the set are earlier or later versions of u with respect to time? To answer this question we compute a so-called node tracking which establishes the time development of all nodes in the graph. Crucially this tracking takes into account topological changes in the evolving graphs. The result of the tracking is stored as node properties of the graphs. Naturally, the program computing the tracking is include in the dataset. To the best of our knowledge, this type of data is made available for the first time through the KIST data set.
Finally, in addition to the actual data, i.e. images and graphs, the KIST Europe data set contains scripts and larger programs used to process and evaluate the data. Suitable configuration files specify the used regions of interest and the parameters used with NEFI. Thus it becomes possible to repeat the entire data production process from the raw images to the obtained filtered graphs including the tracking of nodes.
Subject
Biology; Computer Science, Systems and Electrical Engineering
Related Publication
Michael Dirnberger, Kurt Mehlhorn, and Tim Mehlhorn: Introducing the slime mold graph repository. J. Phys. D: Appl. Phys. 50 264001, 2017https://doi.org/10.1088/1361-6463/aa7326
License/Data Use Agreement
CC BY 4.0
ui-button
FilesMetadataTermsVersions
1 File
KIST_Europe_data_set.zip
ZIP Archive - 422.4 GB
Published May 9, 2025
100 Downloads
MD5: 19faae94810a3a3719663d0a5f2153bc
DATA
Preview "KIST_Europe_data_set.zip"
Access File
File Access
Public
Download Options
ZIP Archive
Download Metadata
Data File Citation
Download EndNote XML
Download RIS
Download BibTeX
Export Metadata
OAI_ORE
DataCite
OpenAIRE
Schema.org JSON-LD
DDI Codebook v2
Dublin Core
DDI HTML Codebook
JSON
Citation Metadata
Persistent Identifier
doi:10.17617/3.XWST2Q
Publication Date
2025-05-09
Title
Slime Mold Graph Repository
Author
Mehlhorn, Tim
KIST Europe
Dirnberger, Michael
Algorithms & Complexity, Max Planck Institute for Informatics
Description
The KIST Europe Data Set
Introduction
This dataset focuses on networks formed by Physarum Polycephalum. Detailed methods are available in the companion paper.
Description
The KIST Europe data set contains raw and processed data of 81 identical experiments, carefully executed under constant laboratory conditions. The data was produced using the following procedure:
A rectangular plastic dish is prepared with a thin sheet of agar.
A small amount of dried P. Polycephalum (HU195xHU200) sclerotia crumbs is lined up along the short edge of the dish. The dish is put into a large light-proof box.
After approximately 14 hours the plasmodium has resuscitated and starts exploring the available space towards the far side of the dish. Typically, the apical zone needs to cover a distance of several centimeters before network formation can be observed properly.
For the next 30 hours we take a top-view image of the growing plasmodium and its changing network every 120 seconds from a fixed position. We stop capturing when the apical zone is about to reach the far side of the dish, which is outside of the observed area.
After obtaining sequences of images showing the characteristic networks of P. Polycephalum, we use a software called NEFI to compute corresponding sequences of graph representations of the depicted structures within a predefined region of interest. In addition to the topology the graphs store precise information of the length and width of the edges as well as the coordinates of the nodes in the plane.
Given the resulting sequence of graphs we apply filters removing artifacts and other unwanted features of the graphs. Then we proceed to compute a novel node tracking, encoding the time development of every node, taking into account the changing topology of the evolving graphs.
Repeating this experiment we obtain 81 sequence of images, which we consider our raw data. We stress at this point that given the inherently uncontrollable growth process of P. Polycephalum, the obtained sequences differ in length and nature. That is to say, in some experiments the organism behaved unfavorably, simply stopping its growth, changing direction or even escaping the container. While such sequences are part of the raw dataset, we excluded them partially or completely from the subsequent graph extraction efforts. The removal of such data reduces the number of series depicting proper network formation to 54.
After obtaining the raw data, we transform the images into equivalent mathematical graphs, thus opening up a wealth of possibilities for data analysis. To this end we deploy a convenient automatic software tool called NEFI, which analyzes a digital image, separates the depicted slime mold network from the background and returns a graph representation of said structure. Using this tool effectively requires some moderate amount of image preprocessing. In particular, for each sequence of images it is necessary to decide on a suitable subsequence to be processed. Here we typically exclude parts of the sequence where the apical zone is still visible. For each such subsequence a suitable region of interest is defined manually. The graph stores the position of the nodes in the plane as well as edge attributes such as edge length and widths for each edge. In addition to the output of NEFI including the unfiltered graphs, the dataset contains NEFI's input, i.e. the selected subsequences of images cropped according to their defined regions of interest.
Note that some parts of the image series showing proper network formation did not yield optimal representations of the depicted networks. This is a result of images exhibiting strong color gradients rendering them too challenging for automatic network extraction. While such cases can still be handled by tuning the parameters of image processing manually on an image per image basis, we decided to discard affected series from subsequent processing efforts. As a result the number of usable graph sequences of highest quality reduced to 36 to which we apply a set of filters removing artifacts, isolated small components and dead-end paths. Thus we obtain a total of 3134 distinct filtered graphs faithfully reflecting the topology and edge attributes that P. Polycephalum displayed during the wet-lab experiments. At this point available graph analysis packages or custom written analysis code can be deployed to investigate the data in various ways. The dataset includes the filtered graphs as well as all corresponding graph drawings. The latter enable a quick visual inspection of the results of the graph extraction.
Given the obtained time-ordered sequences of graphs the development of the entire graph can be investigated. However, one may also study what happens to single nodes as P. Polycephalum evolves. Given a graph in a time ordered sequence of graphs, let us pick any node u. Can we find pick a set of nodes from graphs in the sequence that are equivalent to u, that is, all nodes in the set are earlier or later versions of u with respect to time? To answer this question we compute a so-called node tracking which establishes the time development of all nodes in the graph. Crucially this tracking takes into account topological changes in the evolving graphs. The result of the tracking is stored as node properties of the graphs. Naturally, the program computing the tracking is include in the dataset. To the best of our knowledge, this type of data is made available for the first time through the KIST data set.
Finally, in addition to the actual data, i.e. images and graphs, the KIST Europe data set contains scripts and larger programs used to process and evaluate the data. Suitable configuration files specify the used regions of interest and the parameters used with NEFI. Thus it becomes possible to repeat the entire data production process from the raw images to the obtained filtered graphs including the tracking of nodes.
Subject
Biology; Computer Science, Systems and Electrical Engineering
Language
English
Depositor
Karrenbauer, Andreas
Deposit Date
2025-03-13
Software
NEFI
Related Publication
Michael Dirnberger, Kurt Mehlhorn, and Tim Mehlhorn: Introducing the slime mold graph repository. J. Phys. D: Appl. Phys. 50 264001, 2017 https://doi.org/10.1088/1361-6463/aa7326
Dataset Terms
License/Data Use Agreement
Our Community Norms as well as good scientific practices expect that proper credit is given via citation. Please use the data citation shown on the dataset page.
CC BY 4.0
Direct
Dataset VersionSummaryContributorsPublished onNo records found.Edit File
This file has already been deleted (or replaced) in the current version. It may not be edited.
Close
Restrict Access
Restricting limits access to published files. People who want to use the restricted files can request access by default.
If you disable request access, you must add information about access to the Terms of Access field.
Learn about restricting files and dataset access in the User Guide.
Request Access
Enable access request
You must enable request access or add terms of access to restrict file access.
Terms of Access for Restricted Files
Save Changes
Cancel
Edit EmbargoThe selected file or files have already been published. Contact an administrator to change the embargo date or reason of the file or files.
Cancel
Edit Retention PeriodThe selected file or files have already been published. Contact an administrator to change the retention period date or reason of the file or files.
Cancel
Delete Files
The file will be deleted after you click on the Delete button.
Files will not be removed from previously published versions of the dataset.
Delete
Cancel
Continue
Cancel
Select File(s)
Please select one or more files.
Close
Share Dataset
Share this dataset on your favorite social media networks.
Close
Continue
Cancel
Dataset Citations
Citations for this dataset are retrieved from Crossref via DataCite using Make Data Count standards. For more information about dataset metrics, please refer to the User Guide.
Sorry, no citations were found.
Close
Inaccessible Files Selected
The selected file(s) may not be downloaded because you have not been granted access or the file(s) have a retention period that has expired or the files can only be transferred via Globus.
You may request access to any restricted file(s) by clicking the Request Access button.
Close
Ineligible Files Selected
The selected file(s) may not be transferred because you have not been granted access or the file(s) have a retention period that has expired or the files are not Globus accessible.
You may request access to any restricted file(s) by clicking the Request Access button.
Close
Download Options
The files selected are too large to download as a ZIP.
You can select individual files that are below the 4.7 GB download limit from the files table, or use the Data Access API for programmatic access to the files.
Select File(s)
Please select a file or files to be downloaded.
Close
Inaccessible Files Selected
The selected file(s) may not be downloaded because you have not been granted access or the file(s) have a retention period that has expired.
Click Continue to download the files you have access to download.Continue
Cancel
Ineligible Files Selected
Some file(s) cannot be transferred. (They are restricted, embargoed, with an expired retention period, or not Globus accessible.)
Click Continue to transfer the elligible files.Continue
Cancel
Delete Dataset
Are you sure you want to delete this dataset and all of its files? You cannot undelete this dataset.
Continue
Cancel
Delete Draft Version
Are you sure you want to delete this draft version? Files will be reverted to the most recently published version. You cannot undelete this draft.
Continue
Cancel
Unpublished Dataset Preview URL
Preview URL can only be used with unpublished versions of datasets.
Cancel
Unpublished Dataset Preview URL
Are you sure you want to disable the Preview URL? If you have shared the Preview URL with others they will no longer be able to use it to access your unpublished dataset.
Yes, Disable General Preview URL
Cancel
Delete Files
The file(s) will be deleted after you click on the Delete button.
Files will not be removed from previously published versions of the dataset.
Delete
Cancel
Compute
This dataset contains restricted files you may not compute on because you have not been granted access.
Close
Deaccession Dataset
Are you sure you want to deaccession? This is permanent and the selected version(s) will no longer be viewable by the public.
No
Deaccession Dataset
Are you sure you want to deaccession this dataset? This is permanent an it will no longer be viewable by the public.
No
Version Differences Details
Please select two versions to view the differences.
Close
Version Differences Details
Version:
Last Updated:
Version:
Last Updated:
Done
Select File(s)
Please select a file or files for access request.
Close
Select File(s)
Embargoed files cannot be accessed. Please select an unembargoed file or files for your access request.
Close
Edit Tags
Select existing file tags or create new tags to describe your files. Each file can have more than one tag.
Save ChangesCancel
Request Access
You need to Sign Up or Log In to request access.
Close
Dataset Terms
Please confirm and/or complete the information needed below in order to request access to files in this dataset.
This dataset is made available under the following terms. Please confirm and/or complete the information needed below in order to continue.
License/Data Use Agreement
Our Community Norms as well as good scientific practices expect that proper credit is given via citation. Please use the data citation shown on the dataset page.
CC BY 4.0
Preview Guestbook
Upon downloading files the guestbook asks for the following information.
Guestbook Name
Collected Data
Account Information
Close
Package File Download
Use the Download URL in a Wget command or a download manager to download this package file. Download via web browser is not recommended. User Guide - Downloading a Dataverse Package via URL
Download URL
https://edmond.mpg.de/api/access/datafile/
Close
Compute Batch
Clear Batchui-button
Dataset
Persistent Identifier
Change Compute Batch
Compute Batch
Cancel
Submit for Review
You will not be able to make changes to this dataset while it is in review.
Submit
Cancel
Publish Dataset
Are you sure you want to republish this dataset?
Make sure you have checked legal specifications for export control for academic publications by the German Federal Office for Economic Affairs and Export Control.
Select if this is a minor or major version update.
Minor Release (1.1)Major Release (2.0)
Continue
Cancel
Publish Dataset
This dataset cannot be published until
Edmond
is published by its administrator.
Close
Return to Author
Return this dataset to contributor for modification. The reason for return entered below will be sent by email to the author.
Continue
Cancel
Curation Status HistoryStatusDateAssignerNo records found.Add/Edit a Version Note
Styled Citation