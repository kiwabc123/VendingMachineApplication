export default function ProductCard({ name, price, stock, onSelect, loading,image_url }) {
  return (
    <div className="bg-cafe-surface rounded-xl shadow-soft p-4 flex flex-col">
      {/* image placeholder */}
        <img
        src={image_url}
        alt={name}
        className="h-24 w-24 object-contain mx-auto"
        />

      <h3 className="font-heading text-cafe-primary text-lg text-center">
        {name}
      </h3>

      <p className="text-center text-cafe-muted">
        {price} THB
      </p>

      <button
        onClick={onSelect}
        disabled={stock === 0 || loading}
        className="mt-3 bg-cafe-primary text-white py-1 rounded-lg disabled:opacity-40 hover:bg-cafe-primary/80 transition-colors duration-200 disabled:hover:bg-cafe-primary"
      >
        {stock === 0 ? "Out of stock" : loading ? "Loading..." : "Select"}
      </button>
    </div>
  )
}
