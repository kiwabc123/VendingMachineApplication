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
