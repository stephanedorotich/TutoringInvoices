---
title: TutoringInvoice\invoiceID
author: Stéphane Dorotich
date: \invoiceDate
header-includes:
- \usepackage{tabularx}
documentclass: scrartcl
---

### From:

> Stéphane Dorotich
>
> (587) 434-7693
>
> stephanedorotich@gmail.com

### To:

> \parentName
>
> \parentPhone
>
> \parentEmail
>
> \parentAddr

### Tutoring - \studentName

\begin{center}
\begin{tabularx}{0.9\textwidth}{
>{\raggedright\arraybackslash}X 
>{\centering\arraybackslash}X 
>{\centering\arraybackslash}X 
>{\raggedleft\arraybackslash}X }
\hline
\textit{Session Datetime} & \textit{Duration} & \textit{Rate} & \textit{Cost} \\ [0.75ex] 
\hline
\sessions
[1.0ex]
\hline
\end{tabularx}
\end{center}

### Balance Due: \balanceDue

Payable by: cash, cheque, or e-transfer
