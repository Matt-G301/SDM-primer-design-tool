# SDM-primer-design-tool
When using a site directed mutagenesis protocol (SMD) that will end by assembling a plasmid using Gibson assembly or similar overlap/exonuclease-ligase based assembly this tool will allow you to design the PCR primers using the sequence on the gene for your original plasmid.

The program is written in python and uses tkinter as its GUI -- for other requirements see requirements.txt, openpyxl is a soft requirement, the program will default to saving your primers to a .csv instead of .xlsx without it. The output does not use any features that require a .xlsx file type, so if you need a .xlsx file later just open the .csv in excel and save as .xlsx.

0.0: To run in google colab   NOT YET OPERATIONAL USE A LOCAL INSTALL FOR NOW
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](
https://colab.research.google.com/github/Matt-G301/SDM-primer-design-tool/blob/main/Colab_tool.ipynb
)

0: Type the name of your gene into the Gene name box, or leave it as mutant

1: Simply copy and paste the gene you wish to mutate into the main window
-	If necessary, copy the DNA sequence upstream and downstream of your gene as well (in the construct you want to mutate)
  
2: Next click Log Codons/Basses
-	This will store the sequence in the programs memory, and allow you to select the codon or base you need to mutate by number, instead of risking typos trying to copy the section around your mutation each time you design a primer. 
  
3: Now type in the number of the codon or base you wish to mutate in the "Location in Gene" box, and what you want it changed to in the "Replacement" box, and ensure you are in codon or base mode as needed.

3.5 Setting the minimum TM for the overlap (Min Overlap TM) will ensure that the overlapping region used by your exonuclease/ligase assembly will have a TM above that number. The default is 50 °C as this is the temperature most available master mixes for exonuclease/ligase assembly run at. 
- While rare it may not be possible for the program to find 20 bases of overlap with a TM above 50 °C, in this case you will need to lower the Min Overlap TM and potentially modify your protocol to run the assembly cooler and longer. 

  

4: When ready click "Generate Primers" and if there are no errors they will appear in the boxes below, if you are satisfied with them click "Save to Memory"
  
4.5: Repeat steps 3-4 for any other mutations you want to make. The original intent with this tool was to allow someone to rapidly design primers for multiple mutants being made from one original plasmid (X number of new plasmids 1 mutation each). It remains ideal for this kind of application, saving time and preventing errors when compared to online tools that require you to copy the upstream and downstream sequence from each mutation you want to make.  

5: When you are ready click "Export to Excel" and save your file. Remember this is only the primers saved in the memory so be sure to save the last one you generated and not just leave it on the screen.

6: The exported list is formatted so that it can be uploaded as DNA oligos to Benchling, and placed as a bulk order from IDT (as a .xlsx file not as a .csv the do not accept that file type) from here you can follow your PCR/SDM protocol as normal
