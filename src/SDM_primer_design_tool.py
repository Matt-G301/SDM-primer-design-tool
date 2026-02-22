import tkinter as tk
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog

# Global storage
stored_single_bases = []
stored_codons = []
saved_sequences = []
original_selection = ""
targetTm = 60
final_downstream = ""
final_upstream = ""
overlap_seq_R = ""
overlap_seq_L = ""
highlighted_selection = ""
replacement_seq = ""


CODON_TABLE = {
    # Phenylalanine
    "TTT": "F", "TTC": "F",
    # Leucine
    "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    # Isoleucine
    "ATT": "I", "ATC": "I", "ATA": "I",
    # Methionine (Start)
    "ATG": "M",
    # Valine
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    # Serine
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
    # Proline
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    # Threonine
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    # Alanine
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    # Tyrosine
    "TAT": "Y", "TAC": "Y",
    # Histidine
    "CAT": "H", "CAC": "H",
    # Glutamine
    "CAA": "Q", "CAG": "Q",
    # Asparagine
    "AAT": "N", "AAC": "N",
    # Lysine
    "AAA": "K", "AAG": "K",
    # Aspartate
    "GAT": "D", "GAC": "D",
    # Glutamate
    "GAA": "E", "GAG": "E",
    # Cysteine
    "TGT": "C", "TGC": "C",
    # Tryptophan
    "TGG": "W",
    # Arginine
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
    # Glycine
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    # Stop codons
    "TAA": "*", "TAG": "*", "TGA": "*"
}


#save sequinces
def save_to_memory():
    # Determine the index from the entry
    index_str = entry_index.get()
    if not index_str.isdigit():
        messagebox.showerror("Error", "Index must be a number.")
        return
    index = int(index_str)
    
    original_seq = highlighted_selection.upper()
    replacement = entry_replace.get().strip().upper() or original_seq

    # Metadata needed to name sequence on exort
    saved_sequences.append({
        "upstream": upstream_output.get("1.0", tk.END).strip(),
        "downstream": downstream_output.get("1.0", tk.END).strip(),
        "replacement": replacement,
        "original": original_selection,
        "index": index,
        "gene": gene_name.get(),
    })

    messagebox.showinfo("Saved", "Current sequences saved to memory.")

#Export to excel, this the the only part the requires panda
def export_to_excel():
    if not saved_sequences:
        messagebox.showwarning("Warning", "No sequences to export.")
        return

    data = []
    for record in saved_sequences:
        index = record["index"]
        replacement = record["replacement"]
        original = record["original"]
        gene = record["gene"]

        name_R = f"{gene}_{CODON_TABLE.get(original)}{index}{CODON_TABLE.get(replacement)}_R"
        name_F = f"{gene}_{CODON_TABLE.get(original)}{index}{CODON_TABLE.get(replacement)}_F"

        data.append({"Name": name_R, "Sequence": record["upstream"]})
        data.append({"Name": name_F, "Sequence": record["downstream"]})

    df = pd.DataFrame(data, columns=["Name", "Sequence"])

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    try:
        if file_path.endswith(".xlsx"):
            df.to_excel(file_path, index=False, engine='openpyxl')
        else:
            df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"Exported {len(data)//2} sets of primers to file.")
    except ModuleNotFoundError as e:
        if 'openpyxl' in str(e):
            fallback_path = file_path.rsplit('.', 1)[0] + ".csv"
            df.to_csv(fallback_path, index=False)
            messagebox.showwarning(
                "Missing Dependency",
                f"'openpyxl' not found, so exported as CSV instead:\n{fallback_path}"
            )
        else:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")


# Analyze the sequence
def analyze_sequence():
    raw_main = dna_textbox.get("1.0", tk.END).strip().upper()
    extra_up = extra_upstream_textbox.get("1.0", tk.END).strip().upper()
    extra_down = extra_downstream_textbox.get("1.0", tk.END).strip().upper()

    full_sequence = extra_up + raw_main + extra_down
#empty boxes error
    if not full_sequence:
        messagebox.showwarning("Warning", "No DNA sequence entered.")
        return False
#not a DNA sequince error
    if not all(base in "ATCG" for base in full_sequence):
        messagebox.showerror("Invalid Input", "Sequence must contain only A, T, C, and G.")
        return False
#stores bases an generates codon designations
    global stored_single_bases, stored_codons, extra_up_length
    stored_single_bases = list(full_sequence)
    stored_codons = [raw_main[i:i+3] for i in range(0, len(raw_main), 3) if len(raw_main[i:i+3]) == 3]
    extra_up_length = len(extra_up)

    messagebox.showinfo("Analysis Complete", f"Stored {len(raw_main)} main bases and {(len(raw_main)) // 3} codons.")

# Utility to create collapsible section
def create_collapsible_section(parent, label_text):
    frame = tk.Frame(parent)
    toggle_state = {"shown": False}

    # Toggle handler
    def toggle():
        if toggle_state["shown"]:
            text_box.pack_forget()
            toggle_btn.config(text=f"▼ Show {label_text}")
        else:
            text_box.pack(padx=10, pady=2)
            toggle_btn.config(text=f"▲ Hide {label_text}")
        toggle_state["shown"] = not toggle_state["shown"]

    toggle_btn = tk.Button(frame, text=f"▼ Show {label_text}", command=toggle)
    toggle_btn.pack()
    text_box = tk.Text(frame, height=2, width=60, font=("Courier", 12))
    return frame, text_box

# Tm calculation
def calculate_tm(seq):
    # Uses math for DNA sequinces 14 + bp
    seq = seq.upper()
    gc_count = seq.count('G') + seq.count('C')
    length = len(seq)
    if length == 0:
        return 0
    return 64.9 + 41 * (gc_count - 16.4) / length

# Reverse complament 
def reverse_complement(seq):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C',
                  'a': 't', 't': 'a', 'c': 'g', 'g': 'c'}
    return ''.join(complement.get(base, base) for base in reversed(seq))

# Needed to identify lower case reigons for hilighting inserted bases
def find_lowercase_range(s):
    start = None
    for i, c in enumerate(s):
        if c.islower() and start is None:
            start = i
        if c.isupper() and start is not None:
            return start, i
    if start is not None:
        return start, len(s)
    return None, None


def search_sequence():
    # Many global variables were origonaly deffined here but were needed by so many other functions I made them global, this is why they are defnined and reset
    global targetTm, final_downstream, final_upstream, overlap_seq_R, overlap_seq_L, replacement_seq

    final_downstream = ""
    final_upstream = ""
    mode = var_mode.get()
    index_str = entry_index.get()

    if not index_str.isdigit():
        messagebox.showerror("Error", "Index must be a number.")
        return False
    index = int(index_str) - 1

    # Determine base_index and selected bases based on mode
    if mode == "codon":
        if index < 0 or index >= len(stored_codons):
            messagebox.showerror("Error", f"Codon index out of range (1–{len(stored_codons)})")
            return False
        base_index = extra_up_length + index * 3
        highlight_range = (base_index, base_index + 2)
    else:  # mode == "base"
        if index < 0 or index >= len(stored_single_bases):
            messagebox.showerror("Error", f"Base index out of range (1–{len(stored_single_bases)})")
            return False
        base_index = extra_up_length + index
        highlight_range = (base_index, base_index)
# Fixes the problem of modifications being made to the stored gene and causing issues if you made multiple primers
    
    global original_selection
    original_selection = ''.join(stored_single_bases[highlight_range[0]:highlight_range[1] + 1])
    working_bases = stored_single_bases[:]

    # Apply replacement to the copy only if it is a valid option
    replacement = entry_replace.get().upper()
    if replacement:
        if mode == "codon" and len(replacement) == 3 and all(b in "ATCG" for b in replacement):
            working_bases[base_index:base_index+3] = list(replacement)
        elif mode == "base" and len(replacement) == 1 and replacement in "ATCG":
            working_bases[base_index] = replacement
        else:
            messagebox.showerror("Error", "Invalid replacement input.")
            return False

    # Define overlap region centered on selection based on minimum conditons
    min_overlap_len = 15
    try:
        min_overlap_tm = float(entry_min_tm.get())
    except ValueError:
        messagebox.showerror("Error", "Min Overlap Tm must be a number.")
        return False
    selection_len = highlight_range[1] - highlight_range[0] + 1
    overlap_len = max(min_overlap_len, selection_len)
    
    max_possible_len = len(stored_single_bases)
    # Generate the overlap reigon
    while True:
        extra = (overlap_len - selection_len) // 2
        left = max(0, highlight_range[0] - extra)
        right = min(max_possible_len, highlight_range[1] + 1 + extra + (overlap_len - selection_len) % 2)

        overlap_seq = ''.join(working_bases[left:right])
        if len(overlap_seq) >= min_overlap_len and calculate_tm(overlap_seq) >= min_overlap_tm:
            break

        # Expand if not yet valid
        overlap_len += 1
        if left <= 0 and right >= max_possible_len:
            messagebox.showerror("Error", "Primer length exeeds avalibel area")
            return False  # can't expand further
        if overlap_len >=31 :
            messagebox.showerror("Error", "Overlap greater than 30 bases, try lower temperature")
            return False #outsie the range used by assembly mix

    # Final overlap bounds
    overlap_start = left
    overlap_end = right
    overlap_seq = ''.join(working_bases[overlap_start:overlap_end])
    overlap_seq_L = ''.join(working_bases[left:highlight_range[0]])
    overlap_seq_R = ''.join(working_bases[highlight_range[1] + 1:right])

    # Extend upstream to get total target Tm including overlap
    upstream_tm = 0
    upstream_start = overlap_start
    upstream_prefix = ""
    while upstream_start > 0:
        upstream_start -= 1
        upstream_prefix = working_bases[upstream_start] + upstream_prefix
        upstream_tm = calculate_tm(upstream_prefix + overlap_seq)
        if upstream_tm >= targetTm:
            break
    else:
        messagebox.showerror("Error", "Primer length exeeds avalibel area")
        return False
    # Build upstream sequence
    selection_seq = ''.join(working_bases[highlight_range[0]:highlight_range[1] + 1])
    replacement_seq = entry_replace.get().strip().lower() or selection_seq.lower()
    highlighted_selection = replacement_seq
    final_upstream = upstream_prefix + overlap_seq_L+ highlighted_selection + overlap_seq_R

    # Build downsteam sequence
    tm_upstream_prefix = calculate_tm(upstream_prefix + overlap_seq_L)
    downstream_seq = ""
    tm_down = calculate_tm(overlap_seq)
    downstream_start = overlap_end

    while tm_down < tm_upstream_prefix and downstream_start < len(working_bases):
        if downstream_start < len(working_bases):
            downstream_seq += working_bases[downstream_start]
            downstream_start += 1
        else:
            messagebox.showerror("Error", "Primer length exeeds avalibel area")
            return False
        tm_down = calculate_tm(overlap_seq_R + downstream_seq)
        final_downstream = overlap_seq_L+ highlighted_selection + overlap_seq_R + downstream_seq
    return True


# Run after search to valuidate and generate the sequinces for output
def finalizeAndDisplay():
#Global variables 
    global targetTm, final_downstream, final_upstream, overlap_seq_R, overlap_seq_L, highlighted_selection, replacement_seq  

# Reruns the search with new target Tm if the sequinces are too short
    while len(final_downstream) <= len(overlap_seq_L+ highlighted_selection + overlap_seq_R ):
        targetTm += 1
        search_sequence()

#prepares the output    
    else:
        final_upstream = reverse_complement(final_upstream)
        final_downstream = final_downstream
        targetTm = 60 # This resets for nex time as we progress this far automaticaly once the curent run is done using the target Tm variable
        # Generate output
        upstream_output.delete("1.0", tk.END)
        downstream_output.delete("1.0", tk.END)

        #Make reverse primer
        upstream_output.delete("1.0", tk.END)
        upstream_output.insert(tk.END, final_upstream)
        start, end = find_lowercase_range(final_upstream)
        if start is not None:
            upstream_output.tag_add("replacement", f"1.0 + {start}c", f"1.0 + {end}c")
            upstream_output.tag_config("replacement", foreground="red")
        #Make forward primer
        downstream_output.delete("1.0", tk.END)
        downstream_output.insert(tk.END, final_downstream)
        start, end = find_lowercase_range(final_downstream)
        if start is not None:
            downstream_output.tag_add("replacement", f"1.0 + {start}c", f"1.0 + {end}c")
            downstream_output.tag_config("replacement", foreground="red")

#The button to run the find and replace functions
def searchButtonCommand():
    success = search_sequence()# Prevents loops
    if success:
        finalizeAndDisplay()

# GUI setup
root = tk.Tk()
root.title("Primer Design Tool For SDM")
tk.Label(root, text="Primer Design Tool For SDM", font=("Arial", 14)).pack(pady=5)

tk.Label(root, text="Gene name", font=("Arial", 14)).pack(pady=5)
gene_name = tk.Text(root, height=10, width=60, font=("Courier", 12))
gene_name = tk.Entry(width=10)
gene_name.insert(0, "Mutant")
gene_name.pack()

# Extra upstream input
tk.Label(root, text="Extra Upstream Bases (optional)").pack()
extra_upstream_frame, extra_upstream_textbox = create_collapsible_section(root, "Extra Upstream DNA")
extra_upstream_frame.pack()

# Main sequence
tk.Label(root, text="Gene of Intrest", font=("Arial", 14)).pack(pady=5)
dna_textbox = tk.Text(root, height=10, width=60, font=("Courier", 12))
dna_textbox.pack(padx=10, pady=5)

# Extra downstream input
tk.Label(root, text="Extra Downstream Bases (optional)").pack()
extra_downstream_frame, extra_downstream_textbox = create_collapsible_section(root, "Extra Downstream DNA")
extra_downstream_frame.pack()

# Log button
tk.Button(root, text="Log Codons/Basses", command=analyze_sequence).pack(pady=5)

# Query Section
frame_query = tk.Frame(root)
frame_query.pack(pady=10)

#Loaction selector
tk.Label(frame_query, text="Location in Gene (number)").grid(row=0, column=0, padx=5)
entry_index = tk.Entry(frame_query, width=10)
entry_index.grid(row=0, column=1, padx=5)

#Mode setting
var_mode = tk.StringVar(value="codon")
tk.Radiobutton(frame_query, text="Codon", variable=var_mode, value="codon").grid(row=0, column=2)
tk.Radiobutton(frame_query, text="Base", variable=var_mode, value="base").grid(row=0, column=3)
tk.Button(frame_query, text="Generate Primers", command=searchButtonCommand).grid(row=1, column=2, padx=10)

# Minimum Tm input
tk.Label(frame_query, text="Min Overlap Tm:").grid(row=1, column=5, padx=5)
entry_min_tm = tk.Entry(frame_query, width=10)
entry_min_tm.insert(0, "50")  # Default value
entry_min_tm.grid(row=1, column=6, padx=5)


# Upstream output box
upstream_label = tk.Label(root, text="Reverse primer")
upstream_label.pack()
upstream_output = tk.Text(root, height=3, width=70)
upstream_output.pack()

# Downstream output box
downstream_label = tk.Label(root, text="Forward primer")
downstream_label.pack()
downstream_output = tk.Text(root, height=3, width=70)
downstream_output.pack()

#Replacement button
tk.Label(frame_query, text="Replacement:").grid(row=0, column=5, padx=5)
entry_replace = tk.Entry(frame_query, width=10)
entry_replace.grid(row=0, column=6, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

#Save and Export buttons
tk.Button(button_frame, text="Save to Memory", command=save_to_memory).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Export to Excel", command=export_to_excel).pack(side=tk.LEFT, padx=10)
root.mainloop()
