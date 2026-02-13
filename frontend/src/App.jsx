import { Routes, Route } from 'react-router-dom'
import ReviewLanding from './pages/ReviewLanding'

function App() {
  return (
    <Routes>
      <Route path="/review/:token" element={<ReviewLanding />} />
      <Route path="*" element={
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          fontFamily: "'Inter', sans-serif",
          color: '#64748b'
        }}>
          <p>Automated Review Generator</p>
        </div>
      } />
    </Routes>
  )
}

export default App
