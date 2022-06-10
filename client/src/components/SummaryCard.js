import React from 'react'
import '../styles/SummaryCard.css'
import { DownloadOutlined } from '@ant-design/icons'
import { jsPDF } from "jspdf";

function SummaryCard({ summary }) {
  
  const downloadSummary = () => {
    var doc = new jsPDF();
    let splitText = doc.splitTextToSize(summary['summary'], 180);
    doc.text(15, 20, splitText);

    // Save the PDF
    doc.save(`summary_${summary['filename']}.pdf`);
  }

  return (
    <details>
        <summary>
            <span>{summary['filename']}</span>
            <DownloadOutlined style={{ fontSize: '1.2rem', color: 'var(--primary-color)' }} onClick={downloadSummary}/>
        </summary>
        <p>{summary['summary']}</p>
    </details>
  )
}

export default SummaryCard