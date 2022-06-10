import React from 'react'
import '../styles/Button.css'
import { LoadingOutlined } from '@ant-design/icons';
import { Spin } from 'antd';

function Button({ text, onClick, styles, isLoading }) {
  const antIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />
  
  return (
    <button className={`${!isLoading && 'notLoadingButton'}`}style={styles} onClick={onClick}>
      { text }
      {isLoading && <Spin indicator={antIcon} style={{ marginLeft: '1rem'  }}/>}
    </button>
  )
}

export default Button