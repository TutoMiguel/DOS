from docx import Document
p=r'C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\Canon Maestro de la Union Valinoriana v12 actualizado.docx'
d=Document(p)
with open('tables_out.txt','w',encoding='utf-8') as f:
 for i in [1,2,34,40,47]:
  f.write(f'TABLE {i}\n')
  for row in d.tables[i].rows: f.write(' | '.join(c.text for c in row.cells)+'\n')
