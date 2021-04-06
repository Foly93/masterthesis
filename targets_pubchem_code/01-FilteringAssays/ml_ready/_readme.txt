SUMMARY:
--This directrory contains machine learning ready dataframes! Machine learning ready refers to the presence of inputs as well as targets within the files.
--input refers to the cell painting data and target refers to assay data from pubchem
--Here, the assays and their results respectively, encoded by their pubchem AIDs were overlapped with the cell painting data set of Bray et al (doi.org/10.1093/gigascience/giw014).
--The files might need adjustment, since some informations might be redundant for ML application.
--Also every assay used in subsequent work should be inspected closely for applicability, referring to the meaningfulness of the endpoint.
--These assays were selected based on Data-Size first, and then their category assigned by Pubchem (expert curation).
--Other than that, most assays are related to protein targets and pathways that were predicted to be related to toxicity by Lewis Mervin (doi.org/10.1021/acschembio.6b00538).
--Hence, carefulness should guide any further research using this list.
--This readme informs about the DIRECTORY CONTENT, the PURPOSE OF THIS DIRECTORY, it gives a COMPLETE OVERVIEW OF PROCESSES CONDUCTED TO OBTAIN THE ML-READY ASSAYS and some FURTHER INFORMATION about the Top-XXX Assays in two tables.
--For more information refer to the parent directory and its '_readme.txt' aswell as the executables which are conveniently commented.


DIRECTORY CONTENT:
--Subdirectories
----_less_actives		| Directory that contains the Top-481 Assays; also those which are not active and the executables to filter them out
--Executables
----delete_*.sh			| file that was never executed but resembles steps that were conducted to obtain the final Top-52 Assays
--Files
----AID_list.txt		| list of AIDs of the Top-52 Assays for upload to pubchem to obtain description of those assays
----AID_summary.txt		| Summary of Top-52 Assays that incorporate the description given by pubchem; manually generated
----cp_<AID>.csv		| Whole range of files that contain the ml-ready data of the assay with Pubchem AID <AID> and the Cell Painting data


PURPOSE OF THIS DIRECTORY
--This directory holds the assays outputted from the parent directory.
--To obtain the final set of assays further filtering and manipulation have been performed in this directory.
--First, the compounds can have a pubchem activity rating of 'Active', 'Inactive', 'Inconclusive' or 'Unspecified'. Compounds categorized as the latter two were removed from every given dataset.
--Next, it was important that data were having enough 'Active' Compounds. 100 Active compounds were chosen as a criterion.
--This resulted in 52 assays that are ready to be curated manually for their usability for ML with CP data. They are listed in 'AID_list.txt' and described in 'AID_summary.txt'.
--The Top-481 Assays outputted from the parent directory can be found in the subdirectory '_less_actives/'

COMPLETE OVERVIEW OF PROCESSES CONDUCTED TO OBTAIN THE ML-READY ASSAYS
--The semi-automatically selected 52 Assays, named after their Pubchem AID, meet the following criteria:
----1. The size of the Original Bioassay data needs to be among the biggest file sizes on the Pubchem Public repository (ftp://ftp.ncbi.nlm.nih.gov/pubchem/Bioassay/CSV/Data/)
----2. They have to be related to Toxicity or toxicity targets
----3. The Overlap with the Cell-Painting Assay needs to have at least 100 Compounds labelled 'Active'

--Summary of transformations performed from zero to the 52 selected Assays:
----1. Manual: download the 10 biggest directories from Pubchem Public repository (ftp://ftp.ncbi.nlm.nih.gov/pubchem/Bioassay/CSV/Data/)
----2. Automatic: keep the 100 biggest files in each of the 10 biggest folders for further processing (i.e. Top-1000 Assays which are big in size)
----3. Automatic: generate a list of AIDs of the Top-1000 Assays
----4. Manual: Upload the list to Pubchem to download a description of the Top-1000 Assays
----5. Automatic: Only keep the Assays that are labelled with 'Toxicity' contain a target name present in 'tox_targets.txt', resulting in Top-481 Assays
----6. Automatic: list all unique compounds by their CID present in the Top-481 Assays
----7. Manual: Upload the CID-list and download a description of all compounds, that also contains the InChI-Keys
----8. Automatic: use the CID-description to annotate the Top-481 Assays with their InChI-Keys
----9. Automatic: Overlap all the Assays with the CP-Dataset
----10.Automatic: remove all compounds that are neither labelled 'Active' nor 'Inactive'
----11.Automatic: filter for assays that have 100 compounds labelled 'Active' resulting in Top-52 Assays

FURTHER INFORMATION
Table of Top-52 Assays (can be found in ml_ready/)
PUBCHEM AID	| Number of lines in the file (i.e. Compounds)
----------------+---------------------------------------------
cp_602340.csv	| 21400
cp_651658.csv	| 19003
cp_651610.csv	| 18453
cp_504847.csv	| 9223
cp_720582.csv	| 9055
cp_720648.csv	| 9055
cp_624466.csv	| 9018
cp_588458.csv	| 8968
cp_588852.csv	| 8969
cp_624256.csv	| 8714
cp_624202.csv	| 8580
cp_720504.csv	| 8539
cp_504660.csv	| 8226
cp_651635.csv	| 8162
cp_485270.csv	| 8183
cp_2796.csv	| 8183
cp_2540.csv	| 8143
cp_2599.csv	| 8143
cp_504652.csv	| 8142
cp_504582.csv	| 8133
cp_2156.csv	| 8018
cp_2553.csv	| 8018
cp_2642.csv	| 8018
cp_485313.csv	| 7989
cp_1578.csv	| 7963
cp_1822.csv	| 7964
cp_1529.csv	| 7945
cp_1531.csv	| 7941
cp_2098.csv	| 7852
cp_485314.csv	| 7762
cp_624297.csv	| 7693
cp_588855.csv	| 7688
cp_2216.csv	| 7483
cp_504466.csv	| 7170
cp_504333.csv	| 7125
cp_588334.csv	| 7112
cp_1458.csv	| 7035
cp_1688.csv	| 6973
cp_624296.csv	| 6915
cp_932.csv	| 6820
cp_1030.csv	| 5637
cp_504444.csv	| 5572
cp_894.csv	| 5094
cp_777.csv	| 3743
cp_938.csv	| 2687
cp_2330.csv	| 1884
cp_720532.csv	| 1350
cp_743015.csv	| 532
cp_743012.csv	| 511
cp_743014.csv	| 504
cp_651744.csv	| 505
cp_720635.csv	| 375

Table of Top-481 Assays (can be found in _less_actives/)
PUBCHEM AID	| Number of lines in the file (i.e. Compounds)
----------------+---------------------------------------------
cp_602340.csv	| 21444
cp_651687.csv	| 21144
cp_651723.csv	| 21144
cp_720511.csv	| 19263
cp_651710.csv	| 19126
cp_651704.csv	| 19005
cp_651658.csv	| 19003
cp_651610.csv	| 18589
cp_720574.csv	| 14891
cp_624101.csv	| 12579
cp_504847.csv	| 9718
cp_485290.csv	| 9591
cp_2528.csv	| 9524
cp_651635.csv	| 9393
cp_624172.csv	| 9371
cp_624170.csv	| 9363
cp_1477.csv	| 9157
cp_588856.csv	| 9108
cp_588855.csv	| 9106
cp_602310.csv	| 9106
cp_624202.csv	| 9068
cp_504845.csv	| 9062
cp_720504.csv	| 9044
cp_624171.csv	| 9036
cp_880.csv	| 9028
cp_651768.csv	| 9012
cp_720582.csv	| 9055
cp_720704.csv	| 9055
cp_720648.csv	| 9055
cp_720700.csv	| 9055
cp_743126.csv	| 9055
cp_720596.csv	| 9055
cp_743269.csv	| 9055
cp_651957.csv	| 9038
cp_651699.csv	| 9016
cp_624204.csv	| 9016
cp_602440.csv	| 9016
cp_602429.csv	| 9016
cp_624466.csv	| 9018
cp_624377.csv	| 9018
cp_624416.csv	| 9018
cp_651718.csv	| 9018
cp_624467.csv	| 9018
cp_602396.csv	| 9017
cp_624038.csv	| 9017
cp_624267.csv	| 9017
cp_624125.csv	| 9017
cp_624126.csv	| 9017
cp_624268.csv	| 9017
cp_624040.csv	| 9017
cp_624037.csv	| 9017
cp_624169.csv	| 9017
cp_624127.csv	| 9017
cp_602179.csv	| 8969
cp_651572.csv	| 9014
cp_743255.csv	| 8971
cp_624465.csv	| 8985
cp_624463.csv	| 8978
cp_588458.csv	| 8968
cp_602244.csv	| 8968
cp_602141.csv	| 8968
cp_602229.csv	| 8969
cp_602247.csv	| 8969
cp_588352.csv	| 8969
cp_588852.csv	| 8969
cp_602250.csv	| 8969
cp_588819.csv	| 8969
cp_602163.csv	| 8969
cp_588814.csv	| 8969
cp_588664.csv	| 8969
cp_602248.csv	| 8969
cp_588354.csv	| 8968
cp_485281.csv	| 8919
cp_588473.csv	| 8919
cp_588475.csv	| 8919
cp_624464.csv	| 8877
cp_624256.csv	| 8888
cp_504577.csv	| 8860
cp_624296.csv	| 8796
cp_720551.csv	| 8822
cp_602313.csv	| 8814
cp_602233.csv	| 8783
cp_720553.csv	| 8783
cp_624297.csv	| 8752
cp_651550.csv	| 8772
cp_504707.csv	| 8775
cp_504700.csv	| 8775
cp_504734.csv	| 8775
cp_504411.csv	| 8775
cp_588795.csv	| 8723
cp_651719.csv	| 8710
cp_1471.csv	| 8668
cp_624158.csv	| 8699
cp_1030.csv	| 8608
cp_504810.csv	| 8525
cp_504812.csv	| 8525
cp_485313.csv	| 8507
cp_485314.csv	| 8313
cp_504648.csv	| 8279
cp_2676.csv	| 8280
cp_504462.csv	| 8256
cp_504454.csv	| 8228
cp_504660.csv	| 8226
cp_504466.csv	| 8168
cp_504582.csv	| 8200
cp_504490.csv	| 8200
cp_485270.csv	| 8183
cp_2796.csv	| 8183
cp_504651.csv	| 8179
cp_504333.csv	| 8151
cp_485353.csv	| 8124
cp_485273.csv	| 8143
cp_2540.csv	| 8143
cp_2599.csv	| 8143
cp_504652.csv	| 8142
cp_2174.csv	| 8140
cp_2130.csv	| 8140
cp_2177.csv	| 8140
cp_2057.csv	| 8140
cp_2300.csv	| 8140
cp_2129.csv	| 8140
cp_1899.csv	| 8119
cp_1906.csv	| 8119
cp_1961.csv	| 8078
cp_743397.csv	| 8107
cp_504634.csv	| 8114
cp_504357.csv	| 8114
cp_504326.csv	| 8114
cp_504692.csv	| 8114
cp_2058.csv	| 8064
cp_2013.csv	| 8054
cp_2073.csv	| 8078
cp_1817.csv	| 8078
cp_1566.csv	| 8078
cp_1779.csv	| 8078
cp_2661.csv	| 8053
cp_2029.csv	| 8028
cp_1511.csv	| 8018
cp_2156.csv	| 8018
cp_2239.csv	| 8018
cp_2553.csv	| 8018
cp_2237.csv	| 8018
cp_2227.csv	| 8018
cp_2550.csv	| 8018
cp_2648.csv	| 8018
cp_2642.csv	| 8018
cp_1578.csv	| 7963
cp_2216.csv	| 7959
cp_1700.csv	| 7964
cp_1822.csv	| 7964
cp_1706.csv	| 7964
cp_1825.csv	| 7964
cp_2247.csv	| 7961
cp_1663.csv	| 7940
cp_1529.csv	| 7947
cp_1531.csv	| 7945
cp_1530.csv	| 7945
cp_624246.csv	| 7864
cp_485349.csv	| 7874
cp_2098.csv	| 7879
cp_504444.csv	| 7832
cp_1688.csv	| 7847
cp_504414.csv	| 7856
cp_2675.csv	| 7799
cp_588358.csv	| 7784
cp_1458.csv	| 7673
cp_485347.csv	| 7708
cp_485358.csv	| 7666
cp_485344.csv	| 7665
cp_1868.csv	| 7625
cp_1415.csv	| 7556
cp_588334.csv	| 7171
cp_602252.csv	| 7164
cp_1487.csv	| 6922
cp_731.csv	| 6860
cp_631.csv	| 6860
cp_932.csv	| 6820
cp_920.csv	| 6820
cp_861.csv	| 6820
cp_743445.csv	| 6784
cp_871.csv	| 6771
cp_862.csv	| 6771
cp_894.csv	| 6442
cp_1452.csv	| 6419
cp_485360.csv	| 6321
cp_827.csv	| 5453
cp_803.csv	| 5447
cp_828.csv	| 5447
cp_743093.csv	| 4684
cp_881.csv	| 4634
cp_902.csv	| 3817
cp_748.csv	| 3769
cp_777.csv	| 3743
cp_924.csv	| 3718
cp_619.csv	| 3693
cp_796.csv	| 3590
cp_819.csv	| 3587
cp_802.csv	| 3587
cp_808.csv	| 3528
cp_900.csv	| 3446
cp_889.csv	| 3441
cp_923.csv	| 3446
cp_875.csv	| 3446
cp_892.csv	| 3446
cp_887.csv	| 3437
cp_926.csv	| 3261
cp_938.csv	| 3261
cp_595.csv	| 3187
cp_603.csv	| 3187
cp_436.csv	| 2899
cp_927.csv	| 2850
cp_2322.csv	| 2736
cp_2240.csv	| 1899
cp_2330.csv	| 1899
cp_2275.csv	| 1644
cp_720532.csv	| 1570
cp_504770.csv	| 1185
cp_504865.csv	| 1015
cp_743035.csv	| 625
cp_743094.csv	| 625
cp_743036.csv	| 625
cp_720635.csv	| 625
cp_743222.csv	| 554
cp_743202.csv	| 554
cp_743191.csv	| 554
cp_743223.csv	| 554
cp_743215.csv	| 554
cp_743212.csv	| 554
cp_743014.csv	| 625
cp_743012.csv	| 625
cp_743015.csv	| 625
cp_743083.csv	| 625
cp_743042.csv	| 625
cp_743085.csv	| 625
cp_743033.csv	| 625
cp_743084.csv	| 625
cp_743041.csv	| 625
cp_743086.csv	| 625
cp_743040.csv	| 625
cp_651632.csv	| 625
cp_651634.csv	| 625
cp_720634.csv	| 625
cp_743063.csv	| 625
cp_720637.csv	| 625
cp_743053.csv	| 625
cp_743140.csv	| 625
cp_743139.csv	| 625
cp_743054.csv	| 625
cp_743122.csv	| 625
cp_720516.csv	| 625
cp_743213.csv	| 554
cp_743211.csv	| 554
cp_743225.csv	| 554
cp_743194.csv	| 554
cp_743224.csv	| 554
cp_743203.csv	| 554
cp_588834.csv	| 565
cp_743219.csv	| 554
cp_743199.csv	| 554
cp_743227.csv	| 554
cp_743241.csv	| 554
cp_743226.csv	| 554
cp_743242.csv	| 554
cp_602276.csv	| 528
cp_602277.csv	| 528
cp_651742.csv	| 523
cp_651744.csv	| 523
cp_904.csv	| 457
cp_903.csv	| 450
cp_624044.csv	| 338
cp_624032.csv	| 338
cp_624146.csv	| 328
cp_624455.csv	| 328
cp_588349.csv	| 328
cp_588378.csv	| 328
cp_624148.csv	| 328
cp_624149.csv	| 328
cp_485342.csv	| 328
cp_743205.csv	| 327
cp_720559.csv	| 327
cp_743207.csv	| 327
cp_588379.csv	| 238
cp_504364.csv	| 161
cp_651741.csv	| 153
cp_720636.csv	| 154
cp_651838.csv	| 146
cp_720513.csv	| 153
cp_720514.csv	| 153
cp_588516.csv	| 146
cp_588535.csv	| 146
cp_588537.csv	| 146
cp_588544.csv	| 146
cp_588536.csv	| 146
cp_588541.csv	| 146
cp_588515.csv	| 146
cp_588534.csv	| 146
cp_588543.csv	| 146
cp_720653.csv	| 146
cp_651778.csv	| 146
cp_651777.csv	| 146
cp_720697.csv	| 144
cp_720690.csv	| 135
cp_743021.csv	| 133
cp_720491.csv	| 129
cp_743257.csv	| 118
cp_743256.csv	| 118
cp_743044.csv	| 106
cp_743043.csv	| 106
cp_602194.csv	| 106
cp_602192.csv	| 106
cp_602387.csv	| 102
cp_602385.csv	| 102
cp_624405.csv	| 98
cp_624378.csv	| 93
cp_624379.csv	| 93
cp_588402.csv	| 89
cp_588820.csv	| 89
cp_588824.csv	| 89
cp_651611.csv	| 88
cp_651615.csv	| 88
cp_651613.csv	| 88
cp_651614.csv	| 88
cp_651703.csv	| 85
cp_651705.csv	| 85
cp_720488.csv	| 85
cp_2291.csv	| 84
cp_588794.csv	| 84
cp_588792.csv	| 84
cp_588690.csv	| 82
cp_588691.csv	| 82
cp_651953.csv	| 79
cp_651955.csv	| 79
cp_651785.csv	| 79
cp_651780.csv	| 79
cp_651815.csv	| 75
cp_651813.csv	| 75
cp_651814.csv	| 75
cp_651812.csv	| 75
cp_651994.csv	| 74
cp_720646.csv	| 73
cp_602473.csv	| 72
cp_651787.csv	| 70
cp_651952.csv	| 70
cp_651951.csv	| 70
cp_651783.csv	| 70
cp_602260.csv	| 68
cp_588719.csv	| 66
cp_624300.csv	| 65
cp_651754.csv	| 62
cp_651757.csv	| 62
cp_720506.csv	| 60
cp_720507.csv	| 60
cp_743258.csv	| 60
cp_743261.csv	| 60
cp_624380.csv	| 59
cp_624381.csv	| 59
cp_720588.csv	| 59
cp_720589.csv	| 59
cp_588742.csv	| 56
cp_602193.csv	| 56
cp_602195.csv	| 56
cp_602292.csv	| 52
cp_602441.csv	| 52
cp_602293.csv	| 52
cp_624319.csv	| 52
cp_720524.csv	| 52
cp_720523.csv	| 52
cp_720522.csv	| 52
cp_504375.csv	| 48
cp_504374.csv	| 48
cp_602180.csv	| 45
cp_651593.csv	| 41
cp_651597.csv	| 41
cp_651595.csv	| 41
cp_624479.csv	| 39
cp_588397.csv	| 36
cp_588382.csv	| 36
cp_602199.csv	| 36
cp_602200.csv	| 36
cp_602202.csv	| 36
cp_602201.csv	| 36
cp_602204.csv	| 36
cp_720576.csv	| 35
cp_602270.csv	| 34
cp_624002.csv	| 33
cp_651804.csv	| 32
cp_651803.csv	| 32
cp_504756.csv	| 31
cp_588400.csv	| 31
cp_504719.csv	| 27
cp_720503.csv	| 26
cp_720497.csv	| 26
cp_720499.csv	| 26
cp_602118.csv	| 26
cp_602254.csv	| 25
cp_720498.csv	| 24
cp_602224.csv	| 24
cp_602124.csv	| 24
cp_602125.csv	| 24
cp_720518.csv	| 20
cp_720519.csv	| 20
cp_720517.csv	| 20
cp_624129.csv	| 17
cp_602409.csv	| 17
cp_624322.csv	| 16
cp_602167.csv	| 16
cp_602168.csv	| 16
cp_602166.csv	| 16
cp_602382.csv	| 14
cp_602386.csv	| 14
cp_588524.csv	| 14
cp_588538.csv	| 14
cp_602234.csv	| 13
cp_602236.csv	| 13
cp_602235.csv	| 13
cp_588574.csv	| 12
cp_602367.csv	| 10
cp_504724.csv	| 9
cp_504465.csv	| 7
cp_504488.csv	| 5
cp_504497.csv	| 5
cp_504492.csv	| 5
cp_504501.csv	| 5
cp_485979.csv	| 5
cp_602181.csv	| 5
cp_602380.csv	| 4
cp_602378.csv	| 4
cp_485279.csv	| 4
cp_504687.csv	| 3
cp_485285.csv	| 3
cp_485287.csv	| 3
cp_485278.csv	| 3
cp_485277.csv	| 3
cp_602356.csv	| 2
cp_602427.csv	| 2
cp_485282.csv	| 2
cp_485286.csv	| 2
cp_485283.csv	| 2
cp_485393.csv	| 2
cp_485276.csv	| 2
cp_485540.csv	| 2
cp_588647.csv	| 1
cp_485351.csv	| 1
cp_588599.csv	| 1
cp_485391.csv	| 1
cp_485374.csv	| 1
cp_588600.csv	| 1
cp_588598.csv	| 1
cp_588601.csv	| 1
cp_485337.csv	| 1
cp_602404.csv	| 1
cp_485271.csv	| 1
cp_485369.csv	| 1
cp_485370.csv	| 1
cp_651811.csv	| 1
cp_651810.csv	| 1
cp_485336.csv	| 1
cp_485338.csv	| 1
cp_485301.csv	| 1
cp_504793.csv	| 1
cp_485519.csv	| 1
cp_485520.csv	| 1
cp_485521.csv	| 1
cp_485522.csv	| 1
cp_485523.csv	| 1
cp_485524.csv	| 1
cp_485525.csv	| 1
cp_485526.csv	| 1
cp_485527.csv	| 1
cp_485528.csv	| 1
cp_485980.csv	| 1
cp_485407.csv	| 1
cp_485517.csv	| 1
cp_485518.csv	| 1
cp_743121.csv	| 1
cp_485548.csv	| 1
cp_485529.csv	| 1
cp_485941.csv	| 1
cp_485942.csv	| 1
cp_485943.csv	| 1
cp_485944.csv	| 1

