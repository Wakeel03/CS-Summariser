import 'antd/dist/antd.css';
import { InboxOutlined } from '@ant-design/icons';
import { message, Upload } from 'antd';
import React from 'react';
const { Dragger } = Upload;

const UploadForm = ({ files }) => {
    const uploadedFiles = files

    const props = {
      name: 'file',
      multiple: true,
      accept: ".pdf",
      beforeUpload: (file) => {
        uploadedFiles.push(file)
        return false
      },
    
      onRemove(file) {
        uploadedFiles.splice(uploadedFiles.indexOf(file), 1)
      },
    
      onChange(info) {
        const { status } = info.file;
    
        if (status !== 'uploading') {
        //   console.log(info.file, info.fileList);
        }
    
        if (status === 'done') {
          message.success(`${info.file.name} file uploaded successfully.`);
        } else if (status === 'error') {
          message.error(`${info.file.name} file upload failed.`);
        }
      },
    
      onDrop(e) {
        console.log('Dropped files', e.dataTransfer.files)
      },
    }
    

    return (
        <Dragger {...props} style={{ height: '10%'  }}>
            <p className="ant-upload-drag-icon">
            <InboxOutlined />
            </p>
            <p className="ant-upload-text">Click or drag file to this area to upload</p>
            <p className="ant-upload-hint">
            Upload the PDF of the paper you want to summarize.
            </p>
        </Dragger>
    )
};

export default UploadForm;