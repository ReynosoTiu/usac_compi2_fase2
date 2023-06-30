def reporte(nombre,listaErrores):
    with open('./Archivos/'+nombre+'.html', 'w') as f:
               
        f.write("<html>")
        f.write("<head><title>REPORTE DE ERRORES LEXICOS</title></head>")
        f.write("<body>")
        f.write("<div align=\"center\">")
        f.write("<h1>Reporte de Errores</h1>")
        f.write("<br></br>")
        f.write("<table border=1>")
        f.write("<tr>")
        f.write("<td bgcolor=green>TIPO</td>")
        f.write("<td bgcolor=green>VALOR</td>")
        f.write("<td bgcolor=green>FILA</td>")
        f.write("<td bgcolor=green>COLUMNA</td>")
        f.write("</tr>")
                    
        for i in range(0,len(listaErrores),1):
            f.write("<tr>")
            f.write("<td>"+listaErrores[i].tipo+"</td>")
            f.write("<td>"+listaErrores[i].descripcion+"</td>")
            f.write("<td>"+str(listaErrores[i].fila)+"</td>")
            f.write("<td>"+str(listaErrores[i].columna)+"</td>")
            f.write("</tr>")
                    
        f.write("</table>")
        f.write("</div")
        f.write("</body>")
        f.write("</html>")
                