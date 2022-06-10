import { useRef, useState } from 'react'
import axios from 'axios'
import './styles/App.css'
import Logo from './components/Logo'
import UploadForm from './components/UploadForm'
import Button from './components/Button'
import { CheckCircleOutlined } from '@ant-design/icons'
import SummaryCard from './components/SummaryCard'
import { message } from 'antd';
import jsPDF from 'jspdf'

function App() {

  const URL = 'http://127.0.0.1:5000/'

  const [summaries, setSummaries] = useState([])
  const files = []
  const [isGeneratingSummaries, setIsGeneratingSummaries] = useState(false)
  const numberOfSentencesRef = useRef()

  const summariser = async (e) => {
    e.preventDefault()

    if (files.length === 0) {
      message.error('Please upload a file.')
    }

    let formData = new FormData()

    let numberOfSentences = Math.round(numberOfSentencesRef.current.value)
    if (numberOfSentences < 1) numberOfSentences = 1
    if (numberOfSentences > 20) numberOfSentences = 20

    formData.append('numberOfSentences', numberOfSentences)

    for (let file of files) {
      if (file.type !== 'application/pdf'){
        message.error(`${file.name} is not a PDF file. Please upload only PDF files.`)
        return
      }

      formData.append('file', file)
    }

    try {
      setIsGeneratingSummaries(true)
      const res = await axios.post(URL, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      const sum = res.data.summaries
      setSummaries(JSON.parse(sum))

    }
    catch (error) {
      console.log(error)
    }
    
    setIsGeneratingSummaries(false)
  }

  const downloadAllGeneratedSummaries = (e) => {
    e.preventDefault()

    for (let summary of summaries) {
      let doc = new jsPDF();
      let splitText = doc.splitTextToSize(summary['summary'], 180);
      doc.text(15, 20, splitText);

      // Save the PDF
      doc.save(`summary_${summary['filename']}.pdf`);
    }
  }

  const btnStyles = {
    backgroundColor: 'var(--primary-color)',
    color: '#fff',
    fontWeight: '500',
    fontSize: '1rem',
  }

  const btnReverseStyles = {
    backgroundColor: '#fff',
    color: 'var(--primary-color)',
    fontWeight: '600',
    fontSize: '0.8rem',
    marginLeft: '1rem'
  }

  const uploadPage = (
    <section>
      <div className="app__container">
        <h2>Upload</h2>
        <div className="app__uploadFormContainer">
          <UploadForm files={files} />
        </div>
      </div>

      <div className="app__numberSentences">
        <span>Number of sentences per summary</span>
        <input defaultValue={10} type='number' step='1' min='1' max='20' ref={numberOfSentencesRef}/>
      </div>

      {isGeneratingSummaries && <Button text='Generating Summaries' styles={btnStyles} isLoading={true}/>}
      {!isGeneratingSummaries && <Button text='Generate Summaries' onClick={summariser} styles={btnStyles}/>}
    
    </section>
  )

  const summariesPage = (
    <section>
      <div className="summariesPage__header">
        <div style={{ marginRight: 'auto' }}>
          <CheckCircleOutlined style={{ fontSize: '1.2rem', color: 'green' }}/>
          <span>Summaries Generated</span>
        </div>
        <Button text='Download All' onClick={downloadAllGeneratedSummaries} styles={btnReverseStyles}/>
        <Button text='Upload' onClick={() => setSummaries([])} styles={btnReverseStyles}/>
      </div>

      <div style={{ width: '50%' }} className="">
        {summaries && summaries.map((summary, i) => {
          if (summary['processingError']) {
            message.error(`There was an error processing your file ${summary['filename']}. Please try another PDF.`)
          }

          return (
            <SummaryCard key={i} summary={summary} />
          )
        })}
      </div>

    </section>
  )

  return (
    <main className="app">
      <header>
        <Logo />
      </header>

      {summaries.length > 0 ? summariesPage : uploadPage}

    </main>
  );
}

export default App;
