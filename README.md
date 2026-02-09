# SDM-primer-design-tool
Designs PCR primers for using NEBbuilder or similar product (Like VAzymes clone express) for site directed mutagenesis 

1: Simply coppy and paste the gene you wish to mutate into the main window
  If nesisary, coppy the DNA sequince upstream and downstream of your gene as well (in the construct you want to mutate)
  
2: Next click Log Codons/Basses
  This will store the sequince in the programs memory, and allow you to select the codon or base you need to mutate by number, instead of risking typos trying to coppy the section around your mutation each time you design a primer. 
  
3: Now type in the number of the codon or base you wish to mutate in the "Location in Gene" box, and what you want it changed to in the "Replacement" box, and ensure you are in codon or base mode as needed.

3.5 Settign a minimum overlap TM helps ensure that when you assemble your mutated plasmid later it can work at the temperature your asmebely master mix recomends. Most of these (Clone expres, NEB builder, Gibson) all recomend 50 °C so leaving this on default will normaly be just fine
  it may be nessisary to change this if the program cannot get 20 bases of overlap to reach over 50 °C TM, while rare this can happen and you will need to adjust the minimum TM and mostlikely your protocol

4: When ready click "Generate Primers" and if there are no errors they will apear in the boxes bellow, if you are satisfied with them click "Save to Memory"
  
4.5: Repeat steps 3-4 for any other mutations you want to make, this tool is great for making multiple mutated plasmids from one origonal construct and allowing you to work throught your mutants rapidly

5: when you are ready click "Export to Excel"
  This is what requires the pandas library, it also has a soft requirement for openpyxl to save as .xlsx file type. If you do not have openpyxl it will fall back to a CSV, this is fine as the list of primers dosnt use and features that need a .xlsx file type and you can simple open the .csv in Execel and save as .xlsx later

6: The exported list is formated so that it can be uploaded as DNA oligos to benchling, and placed as a bulk order from IDT (as a .xlsx file not as a .csv the do not accept that file type) from here you can follow your PCR/SDM protocol as normal
