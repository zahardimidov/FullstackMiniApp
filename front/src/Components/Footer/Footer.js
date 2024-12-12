import React from 'react';
import { Link } from "react-router-dom";
import './Footer.css';
import { menu } from './menu';

function Footer({ active = 'Home' }) {
    return (
        <footer>
            <ul className='tabs'>
                {menu.map((tab, idx) => (
                    <li key={`menu item ${idx}`} className={active === tab.text ? 'tab active' : 'tab'}>
                        <Link to={tab.link}>
                            <div className="tab-icon">
                                <img alt={tab.text} src={tab.icon}></img>
                            </div>
                            <span>{tab.text}</span>
                        </Link>
                    </li>
                ))}
            </ul>
        </footer>
    );
}

export default Footer;