
import React from 'react';
import successSVG from '../../Assets/icon/success.svg';
import './Alert.css';

function Alert({ text = 'Alert', timeout = 3, icon = successSVG }) {
    const alertRef = React.useRef(null);

    React.useEffect(() => {
        setTimeout(() => {
            if (alertRef.current) {
                alertRef.current.remove();
            }
        }, (timeout + 1) * 1000)
    })

    return (
        <div className='alert-wrapper' ref={alertRef} style={{ animationDuration: `${timeout}s` }}>
            <div className='alert'>
                <div className='icon-wrapper'>
                    <img src={icon}></img>
                </div>
                <div className='text-wrapper'>
                    <p className='text'>{text}</p>
                </div>
            </div>
        </div>
    );
}

export default Alert;