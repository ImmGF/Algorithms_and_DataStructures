Write a module containing implementations of the following objects:
EditDistance (sequence1, sequence2) - function returning the editing distance of sequence1 and sequence
sequence2.
PhylTree, PhylNode - classes implementing phylogenetic trees for biological sequences and them
nodes labeled with sequences.

We will call elementary editing operations the following text modifications:
substitution - changing a single symbol to another,
deletion - removing a single symbol,
insertion - inserting a single symbol.
The editing distance between two texts is the minimum number of elementary editing operations needed
to transform one text into another. Editing distance is sometimes used as a measure of distance
evolution between homologous biological sequences, e.g. genes or proteins.
