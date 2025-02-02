import Header from './HEADER.jsx';
import Footer from './FOOTER.jsx';
import Card from "./components/Card.jsx";
function App() {
    return(
        <div className="flex justify-center items-center h-screen bg-gray-100">
            <Header/>
                <Card title="React + Tailwind" description="This is a nice styled component!" />
            <Footer/>
        </div>


    );
}

export default App
