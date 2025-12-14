export default function MoneyIcon({ denom }) {
  const colorClass = getColor(denom)
  const isCoin = denom <= 10

  return (
    <div className="flex flex-col items-center">
      {isCoin ? <Coin className={colorClass} /> : <Banknote className={colorClass} />}
    </div>
  )
  function Coin({ className }) {
  return (
    <svg
      viewBox="0 0 48 48"
      className={`w-10 h-10 ${className}`}
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="24" cy="24" r="21.5" />
      <circle cx="24" cy="24" r="14.5" />
      <path d="m24 15c5 0 9 4 9 9" />
    </svg>
  )
}
function Banknote({ className }) {
  return (
    <svg
      viewBox="0 0 64 64"
      className={`w-12 h-10 ${className}`}
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeMiterlimit="10"
    >
      <rect x="1" y="16" width="62" height="32" />
      <path d="M10 44c0-2.8-2.2-5-5-5V25c2.8 0 5-2.2 5-5h44c0 2.8 2.2 5 5 5v14c-2.8 0-5 2.2-5 5H10z" />
      <circle cx="32" cy="32" r="8" />
    </svg>
  )
}


}

const getColor = (denom) => {
  switch (denom) {
    case 1: return "text-amber-700"     // copper
    case 5: return "text-gray-400"      // silver
    case 10: return "text-yellow-500"   // gold
    case 20: return "text-green-600"
    case 50: return "text-blue-500"
    case 100: return "text-red-500"
    case 500: return "text-purple-500"
    case 1000: return "text-amber-900"
    default: return "text-gray-600"
  }
}
