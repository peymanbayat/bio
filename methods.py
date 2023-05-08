from itertools import zip_longest
from textwrap import wrap
import streamlit as st
import re


def sequence_bar():
    text_or_file = ["Enter sequence:", "Upload from .txt file"]
    choice = st.selectbox("Select how you want to enter the sequence",
                          text_or_file)

    if choice == "Upload from .txt file":
        uploaded_file = st.file_uploader("Upload Sequence", type="txt")
        seq = uploaded_file.read()
        seq = seq.decode('UTF-8')
        return seq
    elif choice == "Enter sequence:":
        user_input = st.text_input("Type/paste the sequence", "ATGC")
        return user_input


# counts bases in a string and returns count + sum
def count_bases(seq):
    A = seq.count("A")
    C = seq.count("C")
    G = seq.count("G")
    T = seq.count("T")

    nucleotide_sum = A + C + G + T
    return nucleotide_sum, A, C, G, T

# translates RNA to protein
def translate_to_prot(seq):
    rna_seq = seq.replace("T", "U")
    data = wrap(rna_seq, 3)

    INPUT = ["GCU", "GCC", "GCA", "GCG", "UGU", "UGC", "GAU",
             "GAC", "GAA", "GAG", "UUU", "UUC", "GGG", "GGC",
             "GGA", "GGU", "CAU", "CAC", "AUU", "AUC", "AUA",
             "AAA", "AAG", "UUA", "UUG", "CUA", "CUU", "CUC",
             "CUG", "AUG", "AAU", "AAC", "CCU", "CCC", "CCA",
             "CCG", "CAA", "CAG", "CGU", "CGC", "CGA", "CGG",
             "AGA", "AGG", "UCA", "UCC", "UCG", "UCU", "AGU",
             "AGC", "ACU", "ACA", "ACC", "ACG", "GUU", "GUG",
             "GUA", "GUC", "UGG", "UAU", "UAC"]

    OUTPUT = ["A", "A", "A", "A", "C", "C", "D", "D", "E", "E",
              "F", "F", "G", "G", "G", "G", "H", "H", "I", "I",
              "I", "K", "K", "L", "L", "L", "L", "L", "L", "M",
              "N", "N", "P", "P", "P", "P", "Q", "Q", "R", "R",
              "R", "R", "R", "R", "S", "S", "S", "S", "S", "S",
              "T", "T", "T", "T", "V", "V", "V", "V", "W", "Y",
              "Y"]

    prot_seq = ""

    for bases in data:
        for i, o in zip_longest(INPUT, OUTPUT):
            if i == bases:
                prot_seq += o

    return prot_seq


# mode function - basic DNA analysis
def basic_DNA():
    st.subheader("Analyze your DNA sequence:")

    try:
        seq = sequence_bar()  
        st.text("Your sequence:")
        st.text(seq)

        sum, A, C, G, T = count_bases(seq)

        st.write("There are: ", A, "A ", C, "C",
                 G, "G", T, "T, in total ",
                 sum, " nucleotides")
        st.write("Which is ", round(A/sum*100, 3), "% A ",
                 round(C/sum*100, 3), "% C",
                 round(G/sum*100, 3), "% G",
                 round(T/sum*100, 3), "% T")
        st.write("Which means the GC content is ",
                 round((G+C)/sum*100, 3), "%")

        rna_switch = st.checkbox("1. Show RNA strand?")

        if rna_switch is True:
            st.text(seq.replace("T", "U"))
            translate_prot = st.checkbox("1.1 Translate strand to protein?")

            if translate_prot is True:

                prot_seq = translate_to_prot(seq)

                st.text(prot_seq)

        comp_switch = st.checkbox("2. Show complementary DNA?")

        if comp_switch is True:
            st.text(seq.replace('A', 't').replace('T', 'a').replace('C', 'g')
                    .replace('G', 'c').upper()[::-1])

    except AttributeError:
        pass

# compares original and mutated string to find number of mutations
def find_mutations(origin_seq, mut_seq):
    num_of_mut = 0
    for i in range(0, len(origin_seq)):
        if origin_seq[i] == mut_seq[i]:
            continue
        else:
            num_of_mut += 1
    return num_of_mut

# mode function - count point mutations
def count_point_mut():
    try:
        st.subheader("Original sequence:")
        origin_seq = st.file_uploader("Upload original sequence", type="txt")
        origin_seq = origin_seq.read()
        origin_seq = origin_seq.decode('UTF-8')
        st.text(origin_seq)

    except AttributeError:
        pass

    try:
        st.write("Mutated sequence:")
        mut_seq = st.file_uploader("Upload mutated sequence", type="txt")
        mut_seq = mut_seq.read()
        mut_seq = mut_seq.decode('UTF-8')
        st.text(mut_seq)

    except AttributeError:
        pass

    try:
        num_of_mut = find_mutations(origin_seq, mut_seq)
        st.write("There are ", num_of_mut, " point mutations.")
    except TypeError:
        pass

# mode function - find motifs
def find_motifs():
    try:
        st.subheader("Original sequence:")
        check_motif_seq = sequence_bar()
        st.text(check_motif_seq)

        motif = st.text_input("Write motif sequence below...")

        matches = re.finditer(motif, check_motif_seq)
        positions = [match.start() for match in matches]

        # arrays start at 0 so if I write a list directly it will look ugly
        pos_dict = {}
        for i, pos in enumerate(positions):
            pos_dict[i+1] = pos + 1

        st.write(pos_dict)

    except AttributeError:
        pass
