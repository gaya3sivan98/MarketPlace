import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import api from './services/api'
import './App.css'

function Home() {
  const [services, setServices] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [servicesRes, categoriesRes] = await Promise.all([
          api.get('services/'),
          api.get('categories/')
        ])
        setServices(servicesRes.data)
        setCategories(categoriesRes.data)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <div>Loading marketplace...</div>

  return (
    <div className="container">
      <section className="hero">
        <h1>Find Professional Services Near You</h1>
      </section>

      <section className="categories-section">
        <h2>Service Categories</h2>
        <div className="category-grid">
          {categories.map(category => (
            <div key={category.id} className="category-card">
              <div className="category-icon">
                <i className={`bi ${category.icon}`}></i>
              </div>
              <h3>{category.name}</h3>
            </div>
          ))}
        </div>
      </section>

      <section className="services-section">
        <h2>Available Services</h2>
        {services.length > 0 ? (
          <div className="service-grid">
            {services.map(service => (
              <div key={service.id} className="service-card">
                <h3>{service.title}</h3>
                <p>{service.description}</p>
                <p><strong>Price:</strong> ${service.price}</p>
                <p><strong>Provider:</strong> {service.provider.username}</p>
                <p className="text-muted small">Member since: {new Date(service.provider.date_joined).toLocaleDateString(undefined, { month: 'short', year: 'numeric' })}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-services">
            <p>No services currently featured. Check out our categories!</p>
          </div>
        )}
      </section>
    </div>
  )
}

function App() {
  return (
    <Router>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
        </ul>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  )
}

export default App
