import { useState, useEffect } from "react"
import axios from "axios"
import VendingScreen from "./components/VendingScreen"
import moneyStyle from "./helper/colorChange.jsx"
import MoneyIcon from "./components/MoneyIcon"

// API endpoint configuration
// When running Docker Compose: use http://localhost:8000 (API in container)
// When both frontend and API in Docker: use http://api:8000
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000"


export default function App() {
  const [products, setProducts] = useState([])
  const [moneyStock, setMoneyStock] = useState([])
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [insertedMoney, setInsertedMoney] = useState(0)
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [currentStep, setCurrentStep] = useState(0) // 0: products, 1: payment, 2: success
  const [purchaseResult, setPurchaseResult] = useState(null)

  // Fetch products and money stock on mount
  useEffect(() => {
    fetchProducts()
    fetchMoneyStock()
  }, [])

  const fetchProducts = async () => {
    try {
      const res = await axios.get(`${API_BASE}/products`)
      setProducts(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    }
  }

  const fetchMoneyStock = async () => {
    try {
      const res = await axios.get(`${API_BASE}/money-stock`)
      setMoneyStock(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    }
  }

  const selectProduct = async (product) => {
    setLoading(true)
    setError(null)
    try {
      const res = await axios.post(`${API_BASE}/select-product`, { product_id: product.id })
      setSessionId(res.data.session_id)
      setSelectedProduct(product)
      setInsertedMoney(0)
      setCurrentStep(1) // Move to payment step
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const insertMoney = async (denom) => {
    if (!sessionId) return
    setLoading(true)
    setError(null)
    try {
      const res = await axios.post(`${API_BASE}/insert-money`, { session_id: sessionId, denom })
      setInsertedMoney(res.data.inserted_amount)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const cancelPurchase = () => {
    setSelectedProduct(null)
    setInsertedMoney(0)
    setSessionId(null)
    setCurrentStep(0)
  }

  const confirmPurchase = async () => {
    if (!sessionId) return
    setLoading(true)
    setError(null)
    try {
      const res = await axios.post(`${API_BASE}/confirm`, { session_id: sessionId })
      // const res = {
      //   data: {
      //     "status": "SUCCESS",
      //     "product": {
      //       "id": 4,
      //       "name": "Lemon Tea"
      //     },
      //     "paid": 100,
      //     "price": 20,
      //     "change": 80,
      //     "change_detail": [
      //       {
      //         "denom": 50,
      //         "qty": 1
      //       },
      //       {
      //         "denom": 20,
      //         "qty": 1
      //       },
      //       {
      //         "denom": 10,
      //         "qty": 1
      //       },
      //       {
      //         "denom": 100,
      //         "qty": 1
      //       },
      //       {
      //         "denom": 500,
      //         "qty": 1
      //       },
      //       {
      //         "denom": 1000,
      //         "qty": 1
      //       },
      //       {
      //         "denom": 1,
      //         "qty": 1
      //       },
      //       {
      //         "denom": 5,
      //         "qty": 1
      //       }
      //     ],
      //     "remaining_stock": 26
      //   }
      // }
      setPurchaseResult(res.data)
      setCurrentStep(2) // Move to success step
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const goBackToProducts = () => {
    setCurrentStep(0)
    setSelectedProduct(null)
    setInsertedMoney(0)
    setSessionId(null)
    setPurchaseResult(null)
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-cafe-primary text-white py-4 text-center shadow-soft flex-shrink-0 sticky top-0 z-10">
        <h1 className="font-heading text-2xl">☕ Blue Coffee Vending</h1>
        {currentStep > 0 && (
          <button
            onClick={goBackToProducts}
            className="absolute left-4 top-4 text-white hover:text-cafe-bg transition-colors"
          >
            ← Back
          </button>
        )}
      </header>

      {/* Main */}
      <main className="flex-1 p-6 overflow-hidden">
        {error && <p className="text-cafe-danger mb-4">{error}</p>}

        {/* Step 0: Product Selection */}
        {currentStep === 0 && (
          <div className="h-full">
            <VendingScreen
              products={products}
              onSelect={selectProduct}
              loading={loading}
            />
          </div>
        )}

        {/* Step 1: Payment */}
        {currentStep === 1 && selectedProduct && (
          <div className="max-w-md mx-auto h-full flex flex-col justify-center">
            <div className="bg-cafe-surface rounded-xl shadow-soft p-6">
              <h2 className="font-heading text-cafe-primary text-2xl mb-4 text-center">
                Payment
              </h2>

              <div className="text-center mb-6">
                <p className="text-lg">
                  <strong>{selectedProduct.name}</strong>
                </p>
                <p className="text-cafe-muted">
                  Price: {selectedProduct.price} THB
                </p>
                <p className="text-xl font-bold text-cafe-primary mt-2">
                  Inserted: {insertedMoney} THB
                </p>
              </div>

              <div className="grid grid-cols-3 gap-3 mb-6">
                {[1, 5, 10, 20, 50, 100, 500, 1000].map(v => (
                  <button
                    key={v}
                    onClick={() => insertMoney(v)}
                    disabled={loading || insertedMoney >= selectedProduct.price}
                    className="bg-cafe-primary text-white py-3 px-4 rounded-lg disabled:opacity-50 text-lg font-bold hover:bg-cafe-primary/80 transition-colors duration-200 disabled:hover:bg-cafe-primary"
                  >
                    +{v} THB
                  </button>
                ))}
              </div>

              <div className="flex gap-3">
                <button
                  onClick={cancelPurchase}
                  disabled={loading}
                  className="flex-1 bg-cafe-danger text-white py-3 rounded-lg disabled:opacity-50 hover:bg-red-600 transition-colors duration-200 disabled:hover:bg-cafe-danger"
                >
                  Cancel
                </button>
                <button
                  onClick={confirmPurchase}
                  disabled={loading || insertedMoney < selectedProduct.price}
                  className="flex-1 bg-cafe-success text-white py-3 rounded-lg disabled:opacity-50 hover:bg-green-600 transition-colors duration-200 disabled:hover:bg-cafe-success"
                >
                  {loading ? "Processing..." : "Confirm Purchase"}
                </button>
              </div>
            </div>

          </div>
        )}

        {/* Step 2: Success */}
        {currentStep === 2 && purchaseResult && (
          <div className="max-w-md mx-auto h-full flex flex-col justify-center">
            <div className="bg-cafe-success rounded-xl shadow-soft p-6 text-center text-white">
              <div className="text-6xl mb-4">✅</div>
              <h2 className="font-heading text-2xl mb-2">
                Purchase Successful!
              </h2>
              <p className="mb-4">
                Enjoy your {purchaseResult.product.name}!
              </p>

              {/* Purchase Details */}
              <div className="bg-white bg-opacity-20 rounded-lg p-4 mb-4 text-left">
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <span>Product:</span>
                  <span className="font-bold">{purchaseResult.product.name}</span>
                  <span>Price:</span>
                  <span className="font-bold">{purchaseResult.price} THB</span>
                  <span>Paid:</span>
                  <span className="font-bold">{purchaseResult.paid} THB</span>
                  {purchaseResult.change > 0 && (
                    <>
                      <span>Change:</span>
                      <span className="font-bold">{purchaseResult.change} THB</span>
                    </>
                  )}
                </div>
              </div>

              {/* Change Detail */}
              {purchaseResult.change_detail && purchaseResult.change_detail.length > 0 && (
                <div className="bg-white bg-opacity-20 rounded-lg p- mb-4">
                  <h3 className="font-heading text-lg mb-3">Your Change:</h3>

                  <div className="
                    grid 
                    grid-cols-6 
                    sm:grid-cols-4 
                    md:grid-cols-4 
                    gap-4 
                    justify-items-center
                  px-4
    ">
                    {purchaseResult.change_detail
                      ?.slice()
                      .sort((a, b) => b.denom - a.denom)
                      .map((change, index) => (
                        <div
                          key={index}
                          className="text-center bg-white bg-opacity-30 rounded-xl p-3 w-full max-w-[100px]"
                        >
                          <MoneyIcon denom={change.denom} />
                          <div className="text-lg font-bold mt-1">
                            {change.denom} THB
                          </div>
                          <div className="text-sm opacity-80">
                            x{change.qty}
                          </div>
                        </div>
                      ))}
                  </div>
                </div>
              )}


              <button
                onClick={goBackToProducts}
                className="bg-white text-cafe-success px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-colors"
              >
                Buy Another Drink
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
